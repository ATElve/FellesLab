# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      TODO
@author:       Sigve Karolius
@organization: Department of Chemical Engineering, NTNU, Norway
@contact:      sigveka@ntnu.no
@license:      Free (GPL.v3), although credit is appreciated
@requires:     Python 2.7.x or higher
@since:        18.06.2015
@version:      2.7
@todo 1.0:
@change:
@note:

"""
import os

from FellesBase import FellesBaseClass
from Equipment import Equipment, Pump
from Sensors import Sensor, Temperature, Voltage, Pressure, SensorFrame
from Sensors import Consentration, Humidity
from Controllers import Controller, AlicatFlowController, \
AlicatPressureController, AlicatLiquidController


from GUI import FellesApp, FellesButton, FellesFrame, FellesLabel, FellesTextInput
from SupportClasses import ExtendedRef, GuiUpdater, DataStorage


from subprocess import call

FILE_PATH = '%s/Desktop/'%(os.path.expanduser("~"))

from time import time

# ================================ Class ==================================== #
class MasterClass(object):
    """
    This class is intended to keep track over objects
    """
    App = FellesApp
    # ------------------------------- Method -------------------------------- #
    def __init__(self):
        """
        """
        super(MasterClass, self).__init__()

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Start(cls):
        """
        """
        FellesBaseClass.StartSampling()
        print "Welcome to the FellesLab!"

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Stop(cls):
        """
        """
        FellesBaseClass.StopSampling()
        print "Good Bye"


    # ------------------------------- Method -------------------------------- #
    @classmethod
    def InitGUI(cls):
        """
        TODO: Write a "window configuration file" such that the windows can be
              opened in the position they where closed before.

              This means that "FellesApp" needs a method for saving the window
              positions as well...
        """
        cls.App = FellesApp(cls)
        cls.gui = {}
        for subCls in [Sensor, Equipment, Controller]:
            cls.gui[cls] = subCls.InitGUI()
        
        print "Framework is ready..."
        cls.App.MainLoop()


