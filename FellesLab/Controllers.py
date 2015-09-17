# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab parent classes
@author:       Sigve Karolius and Arne Tobias Elve
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3)
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:
"""
__author__  = "Sigve Karolius & Arne Tobias Elve"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

import wx
from wx.lib.pubsub import pub
from collections import defaultdict
from random import random
from math import floor

from SupportClasses import ExtendedRef, DataStorage
from FellesBase import FellesBaseClass, synchronized
from GUI import FellesFrame, FellesButton, FellesTextInput, FellesLabel, FellesComboBox, FellesSlider, FellesPlainTextInput
from alicat_devices import AlicatFMC

# ================================ Class ==================================== #
class Controller(FellesBaseClass):
    """
    Syntactic sugar...
    """
    __controllers__ = defaultdict(list)
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.__controllers__[self.__class__].append(ExtendedRef(self)) # Add instance to references

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def InitGUI(cls):
        """
        Method creating GUI
        """
        eGUI = {}
        for ref, instnts in cls.__controllers__.iteritems():
            for inst in instnts:
                eGUI[inst['label']] = inst().CreateGUI()

            print "Creating GUI for Controller: '%s'" %ref.__name__

        return eGUI

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        return '<%s.%s controller at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.ID
        )

# =============================== Class ====================================== #
class AlicatController(Controller):
    """ Parent class for **all** alicat measurement devices.
    This class should be inherited by all the alicat subclasses as follwos:

            def AlicatExample(AlicatController):
                ... ..

    This ensures they have the same basic properties, i.e. class/instance
    methods and variables.
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        """
        super(AlicatController, self).__init__(*args, **kwargs)


    # # ------------------------------- Method -------------------------------- #
    # def CreateGUI(self):
    #     """
    #     """
    #     return AlicatFrame(self)

    # ------------------------------- Method -------------------------------- #
    @synchronized
    def CallResource(self):
        return self.resource.readFlowrate(self['channel'])

# =============================== Class ====================================== #
class AlicatFlowController(AlicatController):
    """ MMMMMMM sugar 
    """
    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        """
        super(AlicatFlowController, self).__init__(*args, **kwargs)

        # ------------------------------- Method -------------------------------- #
    def CreateGUI(self):
        """
        """
        return AlicatFrame(self)

# =============================== Class ====================================== #
class AlicatPressureController(AlicatController):
    """
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        """
        super(AlicatPressureController, self).__init__(*args, **kwargs)

        # ------------------------------- Method -------------------------------- #
    def CreateGUI(self):
        """
        """
        return AlicatPressureFrame(self)




# =============================== Class ====================================== #
class AlicatLiquidController(AlicatController):
    """
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, *args, **kwargs):
        """
        """

        super(AlicatLiquidController, self).__init__(*args, **kwargs)


        # ------------------------------- Method -------------------------------- #
    def CreateGUI(self):
        """
        """
        return AlicatLiquidFrame(self)



# =============================== Class ====================================== #
class AlicatFrame(FellesFrame):


    """

                +------------------------------+ 
                |  |  Air  |  Sampl rate 0.5 ^ |
                |                Valve_Opening |
                |   T  298.0  K       |        |
                |   P    1.1  bar     |        |
                |   F   28.3  ml/s    o        |
                |   C    0.5  mg/L    |        |
                |                     -        |
                +------------------------------+

    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, module, parent=None, debug=False, *args, **kwargs):
        """
        """
        self.Module = module

        super(AlicatFrame, self).__init__( title=self.Module['label'] )
    
        self.InitUI()
        self.Show()   # Show frame
       
    def InitUI(self):
        """ Method creating widgets
        """
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        top_sizer = wx.BoxSizer(wx.VERTICAL) # Main sizer, all sizers are added
        title_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains "status"

        center_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains grid and valve
        # valv_sizer = wx.BoxSizer(wx.HORIZONTAL) # 

        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer = wx.GridSizer(rows = 1, cols = 3, hgap = 5, vgap = 3)
        second_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=4, cols=3, hgap=5, vgap=3)
        last_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create labels:
        self.title_sizer = FellesLabel(self.panel)
        # self.combo_box = FellesComboBox(self.panel, id=wx.ID_ANY,
        #                                  # size=wx.DefaultSize,
        #                                  size=wx.Size(100,20),
        #                                  choices=self.Module.resource.FLUIDS.keys(),
        #                                  style=wx.CB_DROPDOWN|wx.CB_READONLY,
        #                                  value="%s"%self.Module.resource.GetGas(),
        #                                  source=self, target=self.Module.resource.ChangeGas,
        #                                  )

        self.smpl_speed = FellesTextInput(self.panel, value='%s' %1,
                                          initial=1, min=0, max=10,
                                          size=wx.Size(100,20),
                                          name='asdf',
                                          inc = 0.1,
                                          target=self.setSampleSpeed,
                                          arg='sample_speed',
                                          source=self )

        #                     )
        self.setPointText = wx.TextCtrl(self.panel, 
                                        size=(140, -1),
                                        value='0.0',
                                        )

        #     )
        self.spButton = wx.Button(self.panel, label= "Confirm")
        # self.combo_box.Disable() # Disable the gas selection combobox
        self.lble_speed = FellesLabel(self.panel, label='Sampling Rate')
        # self.select_gas = FellesLabel(self.panel, label='Select Gas')
        self.set_point = FellesLabel(self.panel, label='Set Point [l/min] Standard')
        

        # Add labels to sizers:
        # first_sizer.Add(self.select_gas,proportion=0, flag= wx.ALIGN_LEFT|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.lble_speed,proportion=0, flag= wx.CENTER|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.set_point, proportion=0, flag=wx.ALIGN_RIGHT|wx.EXPAND, border=5)

        # label_sizer.Add(self.select_gas)

        # second_sizer.Add(self.combo_box, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        # second_sizer.Add(self.lble_speed, proportion=0, flag=wx.EXPAND|wx.ALIGN_RIGHT, border=5)
        second_sizer.Add(self.smpl_speed, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        second_sizer.Add(self.setPointText, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(self.spButton, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)

        

        # Overall arrangement of the panel
        top_sizer.Add(title_sizer, proportion=0, flag=wx.CENTER, border=5)
        top_sizer.Add(wx.StaticLine(self.panel), proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        top_sizer.Add(first_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        top_sizer.Add(second_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        # top_sizer.Add(center_sizer, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        top_sizer.Add(last_sizer, proportion=0, flag=wx.ALIGN_LEFT, border=5)
        # top_sizer.Add(label_sizer,proportion=0)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        self.top_sizer = top_sizer
        self.top_sizer.Fit(self)

        self.spButton.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, e):
        # print e
        print self.setPointText.GetValue()
        val = self.setPointText.GetValue()
        integer = self.TranslateFlowrateToInt(val)
        print 'interger = ',integer
        if integer >= 0 and integer <= 64000:
            self.Module.resource.setFlowrate(integer)
        else:
            print 'You are trying to set a too high flow rate'

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """ Method updating GUI
        """
        self.top_sizer.Layout()

    # ------------------------------- Method --------------------------------- #
    def setFlowrate(self, rate):
        self.Module.resource.setFlowrate(rate)

    # ------------------------------- Method --------------------------------- #
    def setSampleSpeed(self, args, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def ChangeSetpoint(self, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def SelectGas(self, event):
        # print 'Hei du skifter gass!'
        # print 'event = ',event
        self.Module.ChangeGas(event)

    def TranslateIntToFlowrate(self, value):
        return value*5.0/640000


    def TranslateFlowrateToInt(self, value):
        return floor(eval(value)*12800.0)
# =============================== Class ====================================== #
class AlicatPressureFrame(FellesFrame):


    """


    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, module, parent=None, debug=False, *args, **kwargs):
        """
        """
        self.Module = module

        super(AlicatPressureFrame, self).__init__( title=self.Module['label'] )
    
        self.InitUI()
        self.Show()   # Show frame
       
    def InitUI(self):
        """ Method creating widgets
        """
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        top_sizer = wx.BoxSizer(wx.VERTICAL) # Main sizer, all sizers are added
        title_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains "status"

        center_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains grid and valve
        # valv_sizer = wx.BoxSizer(wx.HORIZONTAL) # 

        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer = wx.GridSizer(rows = 1, cols = 3, hgap = 5, vgap = 3)
        second_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=4, cols=3, hgap=5, vgap=3)
        last_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create labels:
        self.title_sizer = FellesLabel(self.panel)
        # self.combo_box = FellesComboBox(self.panel, id=wx.ID_ANY,
        #                                  # size=wx.DefaultSize,
        #                                  size=wx.Size(100,20),
        #                                  choices=self.Module.resource.FLUIDS.keys(),
        #                                  style=wx.CB_DROPDOWN|wx.CB_READONLY,
        #                                  value="%s"%self.Module.resource.GetGas(),
        #                                  source=self, target=self.Module.resource.ChangeGas,
        #                                  )

        self.smpl_speed = FellesTextInput(self.panel, value='%s' %1,
                                          initial=1, min=0, max=10,
                                          size=wx.Size(100,20),
                                          name='asdf',
                                          inc = 0.1,
                                          target=self.setSampleSpeed,
                                          arg='sample_speed',
                                          source=self )
        # self.valvSlder = FellesPlainTextInput(
        #                       self.panel,
        #                       source = self,
        #                       size=wx.Size(100,20),
        #                       value = str(self.Module.resource.GetSetpoint()),
        #                       # initial=float(self.Module.resource.readFlowrate()),
        #                       initial= float(self.Module.resource.GetSetpoint()),
        #                       # min = 0,
        #                       # max = 64000,
        #                       # inc = 640,
        #                       name = 'Setpoint',
        #                       target=self.Module.resource.setFlowrate,
        #                       # target = self.Module.resource.DoNothing(),
        #                     )
        self.setPointText = wx.TextCtrl(self.panel, 
                                        size=(140, -1),
                                        value='0.0',
                                        )
        # self.cnfrmButton = FellesButton(
        #     self.panel,
        #     source = self.valvSlder.GetValue(),
        #     size = wx.Size(100,20),
        #     name = 'button',
        #     label = 'Halla',
        #     target = self.Module.resource.setFlowrate,
        #     )
        self.spButton = wx.Button(self.panel, label= "Confirm")
        # self.combo_box.Disable() # Disable the gas selection combobox
        self.lble_speed = FellesLabel(self.panel, label='Sampling Rate')
        # self.select_gas = FellesLabel(self.panel, label='Select Gas')
        self.set_point = FellesLabel(self.panel, label='Set Point [psia]')
        # self.valvLabel = FellesLabel(self.panel, label='Valve %')
        # self.valvSlder = FellesSlider(self.panel, source=self, target=self.setFlowrate)

        # self.labels = ['lables', 'Pressure', 'Temperature', 'Flow']
        # self.Gridlabels = ['label', 'value', 'unit']
        # self.Grid = { self.labels[0] : {
        #            self.Gridlabels[0]:FellesLabel(self.panel, label='Variable'), 
        #            self.Gridlabels[1]:FellesLabel(self.panel, label='Value'), 
        #            self.Gridlabels[2]:FellesLabel(self.panel, label='Unit'),
        #                  } ,
        #             self.labels[1] : { 
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[1]), 
        #             self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #             self.Gridlabels[2]: FellesLabel(self.panel, label='[bar]'),
        #                  } ,
        #             self.labels[2] : { 
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[2]), 
        #             self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #             self.Gridlabels[2]: FellesLabel(self.panel, label='[K]'),
        #                  } ,
        #             self.labels[3]: {
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[3]), 
        #         self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #         self.Gridlabels[2]: FellesLabel(self.panel, label='[l/min]'),
        #                  } ,
        #               }

        # Add labels to sizers:
        # first_sizer.Add(self.select_gas,proportion=0, flag= wx.ALIGN_LEFT|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.lble_speed,proportion=0, flag= wx.CENTER|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.set_point, proportion=0, flag=wx.ALIGN_RIGHT|wx.EXPAND, border=5)

        # label_sizer.Add(self.select_gas)

        # second_sizer.Add(self.combo_box, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        # second_sizer.Add(self.lble_speed, proportion=0, flag=wx.EXPAND|wx.ALIGN_RIGHT, border=5)
        second_sizer.Add(self.smpl_speed, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        second_sizer.Add(self.setPointText, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(self.spButton, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)

        # second_sizer.Add(self.valvSlder, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        # second_sizer.Add(self.cnfrmButton, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        # first_sizer.Add(self.valvSlder, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)


        # valv_sizer.Add(self.valvLabel, proportion=0, flag=wx.CENTER, border=5)
        # valv_sizer.Add(self.valvSlder, proportion=0, flag=wx.CENTER, border=5)

        # for i,lab in enumerate(self.labels):
        #     for j,glab in enumerate(self.Gridlabels):
        #         if i ==0 or j == 0:
        #             self.Grid[lab][glab].SetFont(wx.Font(pointSize=12, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD, underline=False, faceName=u'Courier', encoding=wx.FONTENCODING_DEFAULT))

        #         grid_sizer.Add(self.Grid[lab][glab], proportion=0, flag=wx.ALL|wx.EXPAND, border=5)

        # center_sizer.Add(grid_sizer, proportion=0, flag=wx.EXPAND, border=5)
        # center_sizer.Add(valv_sizer, proportion=0, flag=wx.ALIGN_RIGHT, border=5)

        # Overall arrangement of the panel
        top_sizer.Add(title_sizer, proportion=0, flag=wx.CENTER, border=5)
        top_sizer.Add(wx.StaticLine(self.panel), proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        top_sizer.Add(first_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        top_sizer.Add(second_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        # top_sizer.Add(center_sizer, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        top_sizer.Add(last_sizer, proportion=0, flag=wx.ALIGN_LEFT, border=5)
        # top_sizer.Add(label_sizer,proportion=0)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        self.top_sizer = top_sizer
        self.top_sizer.Fit(self)

        self.spButton.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, e):
        # print e
        print self.setPointText.GetValue()
        val = self.setPointText.GetValue()
        integer = self.TranslateFlowrateToInt(val)
        print 'interger = ',integer
        if integer >= 0 and integer <= 64000:
            self.Module.resource.setFlowrate(integer)
        else:
            print 'You are trying to set a too high flow rate'

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """ Method updating GUI
        """
        self.top_sizer.Layout()

    # ------------------------------- Method --------------------------------- #
    def setFlowrate(self, rate):
        self.Module.resource.setFlowrate(rate)

    # ------------------------------- Method --------------------------------- #
    def setSampleSpeed(self, args, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def ChangeSetpoint(self, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def SelectGas(self, event):
        self.Module.ChangeGas(event)

    def TranslateIntToFlowrate(self, value):
        return value*100.0/640000


    def TranslateFlowrateToInt(self, value):
        return floor(eval(value)*640)


# =============================== Class ====================================== #
class AlicatLiquidFrame(FellesFrame):


    """


    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, module, parent=None, debug=False, *args, **kwargs):
        """
        """
        self.Module = module

        super(AlicatLiquidFrame, self).__init__( title=self.Module['label'] )
    
        self.InitUI()
        self.Show()   # Show frame
       
    def InitUI(self):
        """ Method creating widgets
        """
        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)

        top_sizer = wx.BoxSizer(wx.VERTICAL) # Main sizer, all sizers are added
        title_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains "status"

        center_sizer = wx.BoxSizer(wx.HORIZONTAL) # Contains grid and valve
        # valv_sizer = wx.BoxSizer(wx.HORIZONTAL) # 

        first_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer = wx.GridSizer(rows = 1, cols = 3, hgap = 5, vgap = 3)
        second_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(rows=4, cols=3, hgap=5, vgap=3)
        last_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create labels:
        self.title_sizer = FellesLabel(self.panel)
        # self.combo_box = FellesComboBox(self.panel, id=wx.ID_ANY,
        #                                  # size=wx.DefaultSize,
        #                                  size=wx.Size(100,20),
        #                                  choices=self.Module.resource.FLUIDS.keys(),
        #                                  style=wx.CB_DROPDOWN|wx.CB_READONLY,
        #                                  value="%s"%self.Module.resource.GetGas(),
        #                                  source=self, target=self.Module.resource.ChangeGas,
        #                                  )

        self.smpl_speed = FellesTextInput(self.panel, value='%s' %1,
                                          initial=1, min=0, max=10,
                                          size=wx.Size(100,20),
                                          name='asdf',
                                          inc = 0.1,
                                          target=self.setSampleSpeed,
                                          arg='sample_speed',
                                          source=self )
        # self.valvSlder = FellesPlainTextInput(
        #                       self.panel,
        #                       source = self,
        #                       size=wx.Size(100,20),
        #                       value = str(self.Module.resource.GetSetpoint()),
        #                       # initial=float(self.Module.resource.readFlowrate()),
        #                       initial= float(self.Module.resource.GetSetpoint()),
        #                       # min = 0,
        #                       # max = 64000,
        #                       # inc = 640,
        #                       name = 'Setpoint',
        #                       target=self.Module.resource.setFlowrate,
        #                       # target = self.Module.resource.DoNothing(),
        #                     )
        self.setPointText = wx.TextCtrl(self.panel, 
                                        size=(140, -1),
                                        value='0.0',
                                        )
        # self.cnfrmButton = FellesButton(
        #     self.panel,
        #     source = self.valvSlder.GetValue(),
        #     size = wx.Size(100,20),
        #     name = 'button',
        #     label = 'Halla',
        #     target = self.Module.resource.setFlowrate,
        #     )
        self.spButton = wx.Button(self.panel, label= "Confirm")
        # self.combo_box.Disable() # Disable the gas selection combobox
        self.lble_speed = FellesLabel(self.panel, label='Sampling Rate')
        # self.select_gas = FellesLabel(self.panel, label='Select Gas')
        self.set_point = FellesLabel(self.panel, label='Set Point [psig]')
        # self.valvLabel = FellesLabel(self.panel, label='Valve %')
        # self.valvSlder = FellesSlider(self.panel, source=self, target=self.setFlowrate)

        # self.labels = ['lables', 'Pressure', 'Temperature', 'Flow']
        # self.Gridlabels = ['label', 'value', 'unit']
        # self.Grid = { self.labels[0] : {
        #            self.Gridlabels[0]:FellesLabel(self.panel, label='Variable'), 
        #            self.Gridlabels[1]:FellesLabel(self.panel, label='Value'), 
        #            self.Gridlabels[2]:FellesLabel(self.panel, label='Unit'),
        #                  } ,
        #             self.labels[1] : { 
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[1]), 
        #             self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #             self.Gridlabels[2]: FellesLabel(self.panel, label='[bar]'),
        #                  } ,
        #             self.labels[2] : { 
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[2]), 
        #             self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #             self.Gridlabels[2]: FellesLabel(self.panel, label='[K]'),
        #                  } ,
        #             self.labels[3]: {
        #         self.Gridlabels[0]: FellesLabel(self.panel, label=self.labels[3]), 
        #         self.Gridlabels[1]: FellesLabel(self.panel, label='0.00'), 
        #         self.Gridlabels[2]: FellesLabel(self.panel, label='[l/min]'),
        #                  } ,
        #               }

        # Add labels to sizers:
        # first_sizer.Add(self.select_gas,proportion=0, flag= wx.ALIGN_LEFT|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.lble_speed,proportion=0, flag= wx.CENTER|wx.EXPAND,border = 5)
        first_sizer.Add(wx.Size(90,25))
        first_sizer.Add(self.set_point, proportion=0, flag=wx.ALIGN_RIGHT|wx.EXPAND, border=5)

        # label_sizer.Add(self.select_gas)

        # second_sizer.Add(self.combo_box, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        # second_sizer.Add(self.lble_speed, proportion=0, flag=wx.EXPAND|wx.ALIGN_RIGHT, border=5)
        second_sizer.Add(self.smpl_speed, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        second_sizer.Add(wx.Size(90,25))
        second_sizer.Add(self.setPointText, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        second_sizer.Add(self.spButton, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)

        # second_sizer.Add(self.valvSlder, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        # second_sizer.Add(self.cnfrmButton, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)
        # first_sizer.Add(self.valvSlder, proportion=0, flag=wx.ALIGN_LEFT|wx.EXPAND, border=5)


        # valv_sizer.Add(self.valvLabel, proportion=0, flag=wx.CENTER, border=5)
        # valv_sizer.Add(self.valvSlder, proportion=0, flag=wx.CENTER, border=5)

        # for i,lab in enumerate(self.labels):
        #     for j,glab in enumerate(self.Gridlabels):
        #         if i ==0 or j == 0:
        #             self.Grid[lab][glab].SetFont(wx.Font(pointSize=12, family=wx.MODERN, style=wx.NORMAL, weight=wx.BOLD, underline=False, faceName=u'Courier', encoding=wx.FONTENCODING_DEFAULT))

        #         grid_sizer.Add(self.Grid[lab][glab], proportion=0, flag=wx.ALL|wx.EXPAND, border=5)

        # center_sizer.Add(grid_sizer, proportion=0, flag=wx.EXPAND, border=5)
        # center_sizer.Add(valv_sizer, proportion=0, flag=wx.ALIGN_RIGHT, border=5)

        # Overall arrangement of the panel
        top_sizer.Add(title_sizer, proportion=0, flag=wx.CENTER, border=5)
        top_sizer.Add(wx.StaticLine(self.panel), proportion=0, flag=wx.ALL|wx.EXPAND, border=5)
        top_sizer.Add(first_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        top_sizer.Add(second_sizer, proportion=0, flag=wx.CENTER|wx.EXPAND, border=5)
        # top_sizer.Add(center_sizer, proportion=0, flag=wx.ALL|wx.CENTER, border=5)
        top_sizer.Add(last_sizer, proportion=0, flag=wx.ALIGN_LEFT, border=5)
        # top_sizer.Add(label_sizer,proportion=0)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        self.top_sizer = top_sizer
        self.top_sizer.Fit(self)

        self.spButton.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, e):
        # print e
        print self.setPointText.GetValue()
        val = self.setPointText.GetValue()
        integer = self.TranslateFlowrateToInt(val)
        print 'interger = ',integer
        if integer >= 0 and integer <= 64000:
            self.Module.resource.setFlowrate(integer)
        else:
            print 'You are trying to set a too high flow rate'

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self, sender=None, args=None):
        """ Method updating GUI
        """
        self.top_sizer.Layout()

    # ------------------------------- Method --------------------------------- #
    def setFlowrate(self, rate):
        self.Module.resource.setFlowrate(rate)

    # ------------------------------- Method --------------------------------- #
    def setSampleSpeed(self, args, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def ChangeSetpoint(self, event):
        print event

    # ------------------------------- Method --------------------------------- #
    def SelectGas(self, event):
        # print 'Hei du skifter gass!'
        # print 'event = ',event
        self.Module.ChangeGas(event)

    def TranslateIntToFlowrate(self, value):
        return value*100.0/640000


    def TranslateFlowrateToInt(self, value):
        return floor(eval(value)*640)


