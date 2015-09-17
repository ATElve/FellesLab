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
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"
#0123456789012345678901234567890123456789012345678901234567890123456789012345678
from time import time, sleep
from SupportClasses import ExtendedRef, DataStorage
from collections import defaultdict
from threading import Thread, Lock
import os
from time import localtime
from calendar import weekday


# ------------------------- Decorator Method ---------------------------- #
def synchronized(func):
    """ Synchronization decorator
    """
    def wrap(f):
        def newFunction(self,*args, **kwargs):

            with self.__class__.LOCK:
                try:
                    return func(self, *args, **kwargs)
                except:
                    print "'%s' instance: '%s'; Failed to read meassurement at time %.2f " %(self.__class__.__name__, self['label'], FellesBaseClass.Timer())
                finally:
                    pass # Just for completeness
        return newFunction
    return wrap


# ================================ Class ==================================== #
class FellesBaseClass(Thread):
    """Class for performing asynchronous sampling
    @summary: The required input is a callable, function or class.
              1. Overwrite the "self.CallResource" method
              2. Implement "__call__(self, *args, **kwargs)"
              
              def fnc():
                
              
    @type MyThread: Inherited class "Thread" 
    @cvar t0:
    @cvar __refs__:
    @cvar __sfer__:
    @cvar SAMPLE:
    @type SAMPLE: bool
    @cvar SAVE:
    @cvar ReStart:
    @cvar lock:
    @cvar FellesMetaData:
    @cvar GuiMetaData:
    @cvar DataProcessing:
    @cvar Data:
    """
    __refs__ = defaultdict(list)
    __sfer__ = {}
    t0 = time()

    SAMPLE = True
    SAVE = False
    ReSTART = False

    LOCK = Lock() # Lock
    FellesMetaData = {
        'idlig' : True, # The gui is updated, but data is not necessarily stored
        'sampling' : False, # The sampling of data should not start imediately
        'label' : None, # Some unique string
        'sample_speed' : 0.5, # Default sampling rate
        'unit' : '[]', # Unit of the sampled data
    } # Dictionary containing default meta data
    GuiMetaData = {
        'plot' : False, # To plot or not to plot...
        'time_span' : 20, # default plot range in seconds
        'color': 'red', # Plot line color
        'pos' : None, # Position of frame
        'size' : None, # Size of frame
        'style' : None, # frame style
    }
    DataProcessing = {
        'signalFiltering' : None, # Noise filter
        'signalProcessing' : None, # filter sensor output, Fourrier(?), Laplace(?)
        'calibrationCurve' : lambda x: x, # Calibration curve
    }

    Data = DataStorage

    # ------------------------------- Method -------------------------------- #
    def __init__(self, resource, resource_settings = {}, meta_data={}, gui_configuration={}, data_processing={}):
        """ 
        @summary : The initialiser for the class. It gets passed whatever the 
                   primary constructor was called with (for example, if it was
                   called x = MyClass(1, {a : '1'}), __init__ will be passed 
                   1 and {a : '1'} as arguments. __init__ is almost universally 
                   used in Python class definitions.

                   Minimal Working Example:
                   -----------------------------------------------------------
                   from FellesLab import FellesBaseClass

                    class Test(object):

                      dct = {'a':1,'b':2}

                      def __call__(self):
                        return 3

                      def __iter__(self):
                        for (key, val) in self.dct.iteritems():
                          yield key, val

                      def __getitem__(self, key):
                        return dct[key]

                    f = Test()
                    a = FellesBaseClass(f)
                   -----------------------------------------------------------

        @param self:
        @param resource:
        @type resource:
        @param resource_settings:
        @param meta_data:
        @param gui_configuration:
        @param data_processing:
        @param args:
        @param kwargs:
        
        @ivar ID:
        @ivar MetaData:
        @ivar data:
        """
        super(FellesBaseClass, self).__init__()

        self.__refs__[self.__class__].append(ExtendedRef(self)) # Add instance to references
        self.__sfer__[hex(id(self))] =  ExtendedRef(self)

        self.ID = hex(id(self)) # ID used to look up objects (Will change for each run!)
        self.resource = resource # This is the reference to the Adam resource

        # Create "metadata" dictionary based on the common FellesMetaData dict
        self.MetaData = { k : v for k,v in self.FellesMetaData.iteritems()}
        # If the arg "meta_data" contains a key that is already in the dict,
        # replace the key with the input. 
        # This way the user can specify soft settings: "label", etc...
        for (k, v) in self.FellesMetaData.iteritems():
            if meta_data.has_key(k):
                self.MetaData[k] = meta_data[k]

        # Check the "resource_settings" from the user. 
        # Loop through all the standard settings (k,v) from the resource.
        for k,v in iter(self.resource):
            # If a one of the keys in the "resource" has been provided as an
            # argument in "resource_settings", the user wants to change
            # this setting.
            #
            # In this event the "resource" will be asked to change the setting
            # and report back.
            if resource_settings.has_key(k):
                self.resource[k] = resource_settings[k]
                # Add the new setting to the "MetaData"
                self.MetaData[k] = self.resource[k]
            # Otherwise, add the un-changed resource setting to "MetaData"
            else:
                self.MetaData[k] = v

        # Now we add plot configurations to the "MetaData"
        for (k, v) in self.GuiMetaData.iteritems():
            if gui_configuration.has_key(k):
                self.MetaData[k] = gui_configuration[k]
            else:
                self.MetaData[k] = v

        for (k, v) in self.DataProcessing.iteritems():
            if data_processing.has_key(k):
                self.MetaData[k] = data_processing[k]
            else:
                self.MetaData[k] = v


        self.data = self.Data(self) # Dict object reading and writing data
        self.start() # target -> sample source -> self

    # ------------------------------- Method -------------------------------- #
    @synchronized
    def CallResource(self, *args, **kwargs):
        return self.resource(*args, **kwargs)

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """ Class
        Instance method executed by "self.start()". 

        This method performs the sampling
        """
        # TODO: Write a decorator @datastorage to allow automatical storage
        #       of the sampled data without an explicit call to data.Update...
        while FellesBaseClass.SAMPLE:
            s = self.CallResource()(self)
            t = FellesBaseClass.Timer()
            self.data.Update(t, s) # Sample resource
            # Go to sleep
            sleep(self['sample_speed'])

        # TODO: Implement method allowing "restart" aka. pause...
        if FellesBaseClass.ReSTART:
            print "Trying again"
            FellesBaseClass.Start()
            self.run()
        else:
            pass

        print "Stopping Thread: '%s' in instance: '%s', base class: '%s'" %(
                                       self['label'], self.__class__.__name__,
                                         self.__class__.__bases__[0].__name__)

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """ 
        @ summary: Allows an instance of a class to be called as a function. 
                   This means that x() is the same as x.__call__().            
        """
        return self


#     def __iter__(self):
#         """
#         """
#         for (key, val) in self.MetaData.iteritems():
#             yield (key, val)

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        """
        @summary : Defines behavior for when an item is assigned to, using the
                   notation:
                                  self[key] = val
 
        @todo: Raise "Key" and "TypeError" when appropriate
        """
        print "Updating '%s' seting from '%s to '%s'"\
                                   %( self['label'], self.MetaData[key], val )

        self.MetaData[key] = val

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        @summary : Defines behavior for when an item is accessed, using the 
                   notation self[key]. 
        @todo : Raise exceptions "TypeError" if the type of the key is wrong KeyError if there is no corresponding value for the key.
        """
        return self.MetaData if not key else self.MetaData[key]

    # ------------------------------- Method -------------------------------- #
    def __str__(self):
        """
        Defines behavior for when str() is called on an instance of your class.
        @TODO Implement
        """
        return "FellesBase"

    # ------------------------------- Method -------------------------------- #
    def __repr__(self):
        """
        Defines behavior for when repr() is called on an instance of your class. 
        The major difference between str() and repr() is intended audience. 
        repr() is intended to produce output that is mostly machine-readable 
        """
        return '<Instance of %s at %s>'%(self.__class__.__name__,
                                          hex(id(self)) )

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Timer(cls):
        """
        Class method returning a timestamp
        """
        return time() - cls.t0

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def StartSampling(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """
        cls.t0 = time()
        cls.SAVE = True

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def PauseThreads(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """
        cls.t0 = time()
        cls.SAMPLE = False

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def StopSampling(cls):
        """
        Class method starting the Execution of the "static method" Exec by 
        setting "START" to "True"
        
        Moreover, it sets the time stamp for the initial time when all sensors
        started sampling
        """
        cls.SAVE = False
        cls.SAMPLE = False
        cls.Data.Save()

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def FindInstance(cls, ID):
        """
        Class method locating a sensor from "__refs__" using a unique string ID
        which was created on object instantiation.

        The method returns an instance of the object whose ID matches the input. 
        """
        for refID in cls.__sfer__.iterkeys():
            if refID == ID:
                return cls.__sfer__[refID]()

