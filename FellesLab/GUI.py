# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Felles lab GUI graphics parent classes
@author:       Sigve Karolius
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

__author__  = "Sigve Karolius"
__email__   = "<firstname><dot><lastname><at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

import wx
from wx.lib.pubsub import pub # pub.sendMessage('identifier', arg=var) pub.subscribe(method, 'identifier')
from time import sleep, time

# from FellesLab.Utils.SupportClasses import ExtendedRef, GuiUpdater
from SupportClasses import ExtendedRef, GuiUpdater

# =============================== Class ====================================== #
class MainFrame(wx.Frame):
    """

    """
    __frames__ = []

    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent, id, title, pos, size, style, MasterClass):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.__frames__.append(ExtendedRef(self))
        self.__class__.MasterClass = MasterClass

        self.InitUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    # ------------------------------- Method --------------------------------- #
    def InitUI(self):

        # adding panel for cross-platform appearance
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.obj = {}

        # adding sizers
        top_sizer       = wx.BoxSizer(wx.VERTICAL)
        title_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer      = wx.GridSizer(rows=1, cols=1) #, hgap=5, vgap=5)
        input_sizer     = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer    = wx.BoxSizer(wx.HORIZONTAL)

        # adding GUI widgets
        self.obj['logo'] = FellesLabel(self.panel, label=\
'''
      O.
       o .
    aaaaaaaa
    "8. o 8"
     8. O 8
     8 o. 8     ooooooooooo       oooo oooo                   ooooo              .o8
  ,adP O .Yba,  `888'    `8       `888 `888                   `888'             "888
 dP". O  o  "Yb  888      .ooooo.  888  888  .ooooo.  .oooo.o  888      .oooo.   888oooo.
dP' O . o .O `Yb 888ooo8 d88' `88b 888  888 d88' `88bd88(  "8  888     `P  )88b  d88' `88b
8^^^^^^^^^^^^^^8 888   " 888ooo888 888  888 888ooo888`"Y88b.   888      .oP"888  888   888
Yb,          ,dP 888     888    .o 888  888 888    .oo.  )88b  888    od8(  888  888   888
 "Ya,______,aP" o888o    `Y8bod8P'o888oo888o`Y8bod8P'8""888P' o888oood8`Y888""8o `Y8bod8P'
   `""""""""'
'''\
)
        self.obj['logo'].SetFont(wx.Font(pointSize=7, family=wx.MODERN,
             style=wx.NORMAL, weight=wx.BOLD, underline=False,
             faceName=u'Courier', encoding=wx.FONTENCODING_DEFAULT))

        # wx.Font has the following signature:
        # wx.Font(pointSize, family, style, weight, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        # family can be:
        # wx.DECORATIVE, wx.DEFAULT,wx.MODERN, wx.ROMAN, wx.SCRIPT or wx.SWISS.
        # style can be:
        # wx.NORMAL, wx.SLANT or wx.ITALIC.
        # weight can be:
        # wx.NORMAL, wx.LIGHT, or wx.BOLD

        # Buttons
        self.start  = FellesButton(self.panel, source=self, target=self.Start,
                                                         label='Start Sampling')
        self.stop = FellesButton(self.panel, source=self, target=self.Stop,
                                                          label='Stop Sampling')
        self.stop.Disable()

        # arranging and sizing the widgets
        grid_sizer.Add(self.obj['logo'], 0, wx.ALL, 5)

        # arrangement of the on/off buttons
        button_sizer.Add(self.start, 0, wx.ALL, 5)
        button_sizer.Add(self.stop, 0, wx.ALL, 5)

        # overall arrangement of the panel
        top_sizer.Add(title_sizer, 0, wx.CENTER)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(grid_sizer, 0, wx.ALL|wx.CENTER, 5)
        top_sizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        top_sizer.Add(button_sizer, 0, wx.ALL|wx.CENTER, 5)

        # assigning the sizer to the panel
        self.panel.SetSizer(top_sizer)

        # fit the sizer to the panel
        # self.Stop(None, None)
        top_sizer.Fit(self)

    # ------------------------------- Method --------------------------------- #
    def Start(self, event):
        """
        GetEventObject
        GetName 'button'
        """

        self.MasterClass.Start()
        event.GetEventObject().Disable()
        pub.sendMessage('DisableSampleRateChange')
        self.stop.Enable()

    # ------------------------------- Method --------------------------------- #
    def __call__(self):
        return self

    # ------------------------------- Method --------------------------------- #
    def Pause(self, event):
        """

        """
        self.MasterClass.StopSampling()
        print event
        event.GetEventObject().Disable()
        pub.sendMessage('DisableSampleRateChange')
        self.OnClose(self)

    # ------------------------------- Method --------------------------------- #
    def Stop(self, event):
        """

        """
        #FellesFrame.SAMPLING = False
        MainFrame.OnClose(self)
        #self.MasterClass.Stop()
        event.GetEventObject().Disable()
        pub.sendMessage('DisableSampleRateChange')


    # ------------------------------- Method --------------------------------- #
    @classmethod
    def OnClose(cls, event):
        """
        1. StopSampling
        2. close...
        """
        FellesFrame.SAMPLING = False
#        MainFrame.OnClose(cls)
        print "Window: '%s', closed by event: '%s'" %(cls.__name__, event.__class__.__name__)
        for frame in cls.__frames__:
            frame().Destroy()

        cls.MasterClass.Stop()
        cls.MasterClass.App.ExitMainLoop()

# =============================== Class ====================================== #
class FellesApp(wx.App):
    """
    App class
    """

    # ------------------------------- Method --------------------------------- #
    def __init__(self, MasterClass):
        super(FellesApp, self).__init__(False)

        self.MasterClass = MasterClass
        self.InitUI()

    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        wx.App.__init__(self)
        frame = MainFrame(None, -1, "Main Frame", (-1,-1), (300,400),\
        wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), self.MasterClass)

        frame.Show()
        self.SetTopWindow(frame)


# =============================== Class ====================================== #
class FellesFrame(wx.Frame):
    """
        Frame Class
    """
    sample_rate = 0.7 # Default sampling rate
    timer = GuiUpdater
    SAMPLING = True

    __refs__ = []

    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent=None, *args, **kwargs):
        self.__refs__.append(ExtendedRef(self)) # Add instance to references

        # Check for title
        if not kwargs.has_key('title'):
            kwargs['title'] = 'Untitled'

        # Check for name
        if not kwargs.has_key('name'):
            kwargs['name'] = 'Un-named'

        # Check for size of frame
        if not kwargs.has_key('size'):
            kwargs['size'] = wx.DefaultSize

        # Check for frame style
        if not kwargs.has_key('style'):
            kwargs['style'] = wx.DEFAULT_FRAME_STYLE

        # Check for frame position
        if not kwargs.has_key('pos'):
            kwargs['pos'] = wx.DefaultPosition

        
        super(FellesFrame, self).__init__(parent, *args, **kwargs)


        self.timer = GuiUpdater(group=None, target=self.UpdateFrame, source=self)

        # Strategies to close the window
#        pub.subscribe(self.OnClose, 'close.all')
        self.Bind(wx.EVT_CLOSE, MainFrame.OnClose)


    # ------------------------------- Method --------------------------------- #
    def CloseMainWindow(self, event):
        MainFrame.OnClose(event)

    # ------------------------------- Method --------------------------------- #
    def __call__(self):
        return self

    # ------------------------------- Method --------------------------------- #
    def InitUI(self):
        NotImplementedError("User interface is not implemented")

    # ------------------------------- Method --------------------------------- #
    def UpdateFrame(self):
        NotImplementedError("Quit method is not implemented")


# =============================== Class ====================================== #
class FellesButton(wx.Button):
    """
    Button Class

    FellesButton(panel, source, target , label )
    args:
      panel (obj) : instance of 'wx.Panel'
      source (obj): obj. instance (e.g. 'self')
      target (obj): callable (method OR function)
      label (str) : label of the button
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, *args, **kwargs):

        # Check for source
        if not kwargs.has_key('source'):
            self.source = None
        else:
            self.source = kwargs['source']
            del kwargs['source']

        # Check for target, provide dummy output if there is none
        if not kwargs.has_key('target'):
            import DummyOutput
            self.target = DummyOutput.DummyButton()
        else:
            self.target = kwargs['target']
            del kwargs['target']

        # Names and shit...
        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        if not kwargs.has_key('label'):
            kwargs['label'] = 'No Label'

        # Create button
        super(FellesButton, self).__init__(*args, **kwargs)
        # Bind button to an event executed on click
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    # ------------------------------- Method --------------------------------- #
    def OnButtonClicked(self, event):
        """
        Method executed on click
        """
        self.target(event)

    # ------------------------------- Method --------------------------------- #
    def __call__(self):
        """
        Method for calling button programatically, i.e. button()
        """
        self.OnButtonClicked(self)

# =============================== Class ====================================== #
class FellesComboBox(wx.wx.ComboBox):
    """
    Class
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent = None, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

        self.arg = None
        if kwargs.has_key('arg'):
            self.arg = kwargs['arg']
            del kwargs['arg']

        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        if not kwargs.has_key('max'):
            kwargs['max'] = 1

        if not kwargs.has_key('min'):
            kwargs['min'] = 0

        if not kwargs.has_key('initial'):
            kwargs['initial'] = kwargs['min']

        if not kwargs.has_key('value'):
            kwargs['value'] = '%f' %(kwargs['initial'])

        if not kwargs.has_key('inc'):
            kwargs['inc'] = 0.01

        super(FellesTextInput, self).__init__(parent, *args, **kwargs)

#        self.Bind(wx.EVT_SPINCTRL, self.OnSetpointChange)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSetpointChange)

    # ------------------------------- Method --------------------------------- #
    def OnSetpointChange(self, event):
        if not self.arg:
            self.target(event.GetEventObject().GetValue())
        else:
            print 'self.arg = ',self.arg
            self.target(self.arg, event.GetEventObject().GetValue())


# =============================== Class ====================================== #
class FellesTextInput(wx.SpinCtrlDouble): #(wx.SpinCtrl):
    """
    Class

    args:
        target
        source
        min
        max
        initial
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent = None, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

        self.arg = None
        if kwargs.has_key('arg'):
            self.arg = kwargs['arg']
            del kwargs['arg']

        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        if not kwargs.has_key('max'):
            kwargs['max'] = 1

        if not kwargs.has_key('min'):
            kwargs['min'] = 0

        if not kwargs.has_key('initial'):
            kwargs['initial'] = kwargs['min']

        if not kwargs.has_key('value'):
            kwargs['value'] = '%f' %(kwargs['initial'])

        if not kwargs.has_key('inc'):
            kwargs['inc'] = 0.01

        super(FellesTextInput, self).__init__(parent, *args, **kwargs)

#        self.Bind(wx.EVT_SPINCTRL, self.OnSetpointChange)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSetpointChange)

    # ------------------------------- Method --------------------------------- #
    def OnSetpointChange(self, event):
        if not self.arg:
            self.target(event.GetEventObject().GetValue())
        else:
            # print 'self.arg = ',self.arg
            self.target(self.arg, event.GetEventObject().GetValue())
            # self.target(event.GetEventObject().GetValue())

# =============================== Class ====================================== #
class FellesPlainTextInput(wx.TextCtrl): #(wx.SpinCtrl):
    """
    Class

    args:
        target
        source
        min
        max
        initial
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent = None, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

        self.arg = None
        if kwargs.has_key('arg'):
            self.arg = kwargs['arg']
            del kwargs['arg']

        if not kwargs.has_key('name'):
            kwargs['name'] = self.source.GetName()

        # if not kwargs.has_key('max'):
        #     kwargs['max'] = 1

        # if not kwargs.has_key('min'):
        #     kwargs['min'] = 0

        if not kwargs.has_key('initial'):
            kwargs['initial'] = kwargs['min']

        if not kwargs.has_key('value'):
            kwargs['value'] = '%f' %(kwargs['initial'])

        # if not kwargs.has_key('inc'):
        #     kwargs['inc'] = 0.01

        super(FellesPlainTextInput, self).__init__(parent, *args, **kwargs)

#        self.Bind(wx.EVT_SPINCTRL, self.OnSetpointChange)
        # self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnSetpointChange)

    # ------------------------------- Method --------------------------------- #
    # def OnSetpointChange(self, event):
    #     if not self.arg:
    #         self.target(event.GetEventObject().GetValue())
    #     else:
    #         # print 'self.arg = ',self.arg
    #         self.target(self.arg, event.GetEventObject().GetValue())
            # self.target(event.GetEventObject().GetValue())

# =============================== Class ====================================== #
class FellesSlider(wx.Slider):
    """
    Class
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent = None, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

        super(FellesSlider, self).__init__(parent, id=wx.ID_ANY, value=0, minValue=0, maxValue=100, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.SL_MIN_MAX_LABELS|wx.SL_INVERSE|wx.SL_RIGHT, validator=wx.DefaultValidator, name="SliderNameStr")

        self.Bind(wx.EVT_SLIDER, self.OnSelect)

    # ------------------------------- Method --------------------------------- #
    def OnSelect(self, event):
        self.target(event.GetEventObject().GetValue())

# =============================== Class ====================================== #
class FellesComboBox(wx.ComboBox):
    """
    Class
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, parent = None, *args, **kwargs):

        self.source = kwargs['source']
        self.target = kwargs['target']
        del kwargs['target']
        del kwargs['source']

#        ComboBox(parent, id=ID_ANY, value="", pos=DefaultPosition,
#         size=DefaultSize, choices=[], style=0, validator=DefaultValidator,
#         name=ComboBoxNameStr)

        super(FellesComboBox, self).__init__(parent, *args, **kwargs)

        self.Bind(wx.EVT_COMBOBOX, self.OnSelect)

    # ------------------------------- Method --------------------------------- #
    def OnSelect(self, event):
        self.target(event.GetEventObject().GetValue())


# =============================== Class ====================================== #
class FellesLabel(wx.StaticText):
    """
    Sugar class.
    
    TODO: expand class to make it easier to change font
    """
    # ------------------------------- Method --------------------------------- #
    def __init__(self, *args, **kwargs):
        super(FellesLabel, self).__init__(*args, **kwargs)

