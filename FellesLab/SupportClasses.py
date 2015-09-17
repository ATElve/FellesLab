# -*- coding: ascii -*-
"""
oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:
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

import os
import collections
import weakref
import wx
from calendar import weekday
from time import sleep, time, localtime
from threading import Thread
import csv
import itertools as it

from tempfile import TemporaryFile

FILE_PATH = '%s/Desktop/'%(os.path.expanduser("~"))

BACKUP_README = \
'''
# Welcome to the FellesLab "backup system"

This document briefly describes how the output from an experiment is saved, and how a backup may be created.
Please note that this is not a sophisticated backup system.
The output is file saved on the desktop and a backup file is created as long as the student pushes "Stop Sampling".
In the event that the user "closes" the program using the "`X`" button, a backup is **not** created.
Let us say that together, "If I do not push the Stop Sampling button I will not have a backup. When this happens there is **no** way of retrieving the data and I will not receive any sympathy from the software developer."

**Note:**

*The entire "backup directory" can be deleted when the lab is completed.* All sub-directories and files are created **automatically** (yes, that includes "FellesLab_Backup").

---
    oooooooooooo       oooo oooo                    ooooo                 .o8
    `888'     `8       `888 `888                    `888'                "888
     888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
     888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
     888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
     888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
    o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'

                             Sigve Karolius

                   Department of Chemical Engineering
             Norwegian University of Science and Technology

                                .            .
                               / \          / \
                              /   \   /\   /   \
                              |   |  /  \  |   |
                       .______|   |_/    \_|   |______.
                     _/                                \_
          /\        |                                    |        /\
    _____/  \  _____|                                    |_____  /  \_____
             \/                                                \/
---

# Conventions

* **File names:** The file names are generated automatically using the following convention: `Day_Month_Num_HourMinSecond_Year`, e.g. `Sun_Aug_2_221728_2015.csv`.

* **Directory names:** The directories are created automatically as: `Day_Num_Month_Year`, e.g. `Sun_2_Aug_2015`.

* **File format:** The data is saved in a tabular [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format.

* **Data storage format:**  The following example shows how two sensors _Rnd_ and _Rand 2_ both have a _time_ column associated with them. Please note (and appreciate) that even though every sensor has a individual time column, the reference time is identical.
```FILE.csv
    time, Rnd, time, Rand 2
    0.000006 , 0.631032, 0.000002 , 0.124725
    0.001157 , 0.992647, 0.328444 , 0.293643
    0.104696 , 0.711614, 0.830970 , 0.643257
    0.207081 , 0.108123, 1.334370 , 0.354398
    0.309923 , 0.518604, NA , NA
    0.411372 , 0.809855, NA , NA
    0.512407 , 0.558416, NA , NA
    0.613994 , 0.660687, NA , NA
```
* **Data _Not Available_:** When data is *not available* the string **NA** is used. This is the convention for to denote missing data in the **R** programming language. Consequently, this makes importing/plotting data remarkably simple.

* **Data processing example in R:** The file above can be plotted (and saved as a png) using **R** using very few lines:

```R
    csvFile = read.csv('path/to/FILE.csv', header=True) # Read file

    png(filename='path/to/FILE.png', width = 480, height = 480) # Save as png

    plot(csvFile$time, csvFile$Rnd, col="magenta", xlab="time", ylab="Random number", frame=FALSE, pch=1) # Create plot canvas
    points(csvFile$Time.1, csvFile$Rand.2, col="cyan", pch=19) # Add second plot to canvas
    legend("topleft", c("Rnd","Random"), pch=c(1,19), lty=c(NA,NA), col=c("magenta", "cyan"), bty="n") # Legend
    dev.off() # Produce plot output

    summary(csvFile) # Take a look at a statistical summary
```
'''

# ================================ Class ==================================== #
class GuiUpdater(Thread):
    """
    Thread for updating GUI
    """
    
    # ------------------------------- Method -------------------------------- #
    def __init__(self, source, target, *args, **kwargs):
        self.target = target
        self.source = source

        super(GuiUpdater, self).__init__(None)

    # ------------------------------- Method -------------------------------- #
    def run(self):
        """
        Method started when "instance.start()" is called

        The thread will call "source.target()" at a rate determined by "sample
        rate" in the caller.

        NOTE: It is necesary to call target trough wx.CallAfter on Linux.
         "wx.CallAfter(self.target, self)" is a synonym for "self.taget(self)"
        """

        while self.source.SAMPLING:
            wx.CallAfter(self.target, self)
            sleep(0.75)

        self.Terminate()

    # ------------------------------- Method -------------------------------- #
    def Terminate(self):
        """

        """
        print "Stopping GUI thread: '%s', instance: '%s', base class: '%s'" %(
                                                       self.source.GetLabel(),
                                               self.source.__class__.__name__,
                                  self.source.__class__.__bases__[0].__name__,
                                  )
        print "Stopping GUI thread: '%s'" %self.source.GetLabel()
        self.source.OnClose(self)

# ================================ Class ==================================== #
class ExtendedRef(weakref.ref):
    """
    Weakreference class, creates an alias to "referee".

    Understand the class works by considering the following example:

        example.py
        ----------------------------------------------------------------------
        import weakref

        class ExtendedRef(weakref.ref):

            def __init__(self, referee, callback=None):
                self.referee = referee
                super(ExtendedRef, self).__init__(referee, callback)

            def __call__(self):
                return self.referee()

        class Referee:
            message = "References are clever"

            def __call__(self):
                return self

            def ChangeMessage(self, msg):
                self.message = msg

        a = Referee()
        b = ExtendedRef(a)

        print b().message
        b().ChangeMessage("A different message")
        print a.message
        ----------------------------------------------------------------------
    """

    # ------------------------------- Method -------------------------------- #
    def __init__(self, referee, callback=None):
        self.referee = referee
        super(ExtendedRef, self).__init__(referee, callback)

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        """
        Magic method.

        Returns the object that the class referes to. The practical
        implication is that it becomes possible to access the objects methods
        and variables through the reference class.
        """
        return self.referee()

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        """
        Synonymous of calling "__getitem__" in the referee instance
        """
        return self()[key]

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        """
        Synonymous of calling "__setitem__" in the referee instance
        """
        self()[key] = val

    # ------------------------------- Method -------------------------------- #
    def GetID(self):
        """
        Returns "ID" of the referee object
        """
        return hex(id(self()))


# =============================== Class ===================================== #
class DataStorage(object):
    """
    This should have been be a clever data storage container.
    """

    # List of object instances
    __refs__ = []

    # ------------------------------- Method -------------------------------- #
    def __init__(self, owner):
        """
        args:
          owner (instance): Parent object to which the DataStorage instance belongs
        """
        self.__refs__.append(ExtendedRef(self)) # Add instance to references

        self.owner = owner#FindSensor.FindID(ownerID) # Object whose data will be saved
        
        self.File = TemporaryFile()
        self.File.write('time, %s %s\n' %(self.owner['label'], 
                                          self.owner['unit']))

        self.Resize()

    # ------------------------------- Method -------------------------------- #
    def Scale(self, val):
        # return val # self.owner['calibrationCurve'](val)
        return self.owner['calibrationCurve'](val)


    # ------------------------------- Method -------------------------------- #
    def Resize(self):
        """
        Resize the array needed to store

        Use this method if the sample rate is changed.
        """

        self.history_length = int( round( self.owner['time_span']/self.owner['sample_speed']))
        self.FreshStart()

    # ------------------------------- Method -------------------------------- #
    def FreshStart(self):
        """
        Use this method if you just need a fresh start
        """
        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of different are
        # sensors may vary.

        self.history = {'time': collections.deque( [], self.history_length ),\
                        'data': collections.deque( [], self.history_length )
                       }

    # ------------------------------- Method -------------------------------- #
    def Restart(self, time, val):
        """
        """
        # Create a vector holding historical data for the purpose of plotting.
        # The length may vary because the sampling speed of different are
        # sensors may vary.

        self.FreshStart()     
        self.Update(time, val)

    # ------------------------------- Method -------------------------------- #
    def Update(self, time, val):
        """ Method updating the history
        """
        # self['data'] = val #self.owner['calibrationCurve'](val)
        try:
            self['data'] = self.owner['calibrationCurve'](val)
        except:
            self['data'] = 0.0
        # self['data'] = self.owner['calibrationCurve'](val)
        self['time'] = time

        if self.owner.SAVE:
            self.File.write('%f , %f\n' %(time, self['data'][-1] ))

    # ------------------------------- Method -------------------------------- #
    def __call__(self):
        return self

    # ------------------------------- Method -------------------------------- #
    def __getitem__(self, key):
        return self.history if not key else self.history[key]

    # ------------------------------- Method -------------------------------- #
    def __setitem__(self, key, val):
        self.history[key].append(val)

    # ------------------------------- Method -------------------------------- #
    @classmethod
    def Save(cls):
        """
        # Choose wether __refs__ contains id's
        """
        print "Saving data..."
        # Check if the backup directory exists
        backup_dir = FILE_PATH + "FellesLab_Backup"
        if not os.path.isdir(backup_dir):
            os.mkdir(backup_dir)
            with open( backup_dir + "/README", 'w') as f:
                f.write(BACKUP_README)

            #cmd = "python -m markdown {dir}/README > {dir}/README.html".format(dir=backup_dir)
            #call([cmd])
        # Check if the Backup directory has a directory for "today"
        day = FILE_PATH + "FellesLab_Backup/" + cls.dayStamp()
        if not os.path.isdir(day):
            os.mkdir(day)

        # Save data for all the sensors
        # TODO: Rewrite, difficult to follow...
        DATA = [ ] # This will become a list of lists, e.g.
                   # [ [time, ...], [Temp1, ...], [time, ...], [Temp2, ...] ]
        for ref in cls.__refs__:

            ref().File.seek(0) # Rewind file pointer

            F = csv.reader(ref().File, delimiter=',', quotechar='|')
            r = [[],[]]
            for row in F:
                for i,num in enumerate(row):
                    r[i].append(num)
                    if i > 1:
                        r[i].append(float(num))

            for j in r:
                DATA.append(j)
            ref().File.close()

        # Finally, write data file.
        with open( day + "/" + cls.timeStamp() + '.csv', 'w') as f:
            csv.writer(f).writerows( it.izip_longest(*DATA, fillvalue='NA') )

    # ------------------------------- Method -------------------------------- #
    @staticmethod
    def timeStamp():
        """
        Function returning a timestamp (string) in the format:
                        Wed_Jun_17_hourminsec_year
        """
        LT = localtime() # Timestamp information for filename
        Day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        Mon = ['Jan','Feb','Mar','Apr','May','Jun',\
               'Jul','Aug','Sep','Oct','Nov','Dec']
        return '{D}_{M}_{d}_{h}{m}{s}_{Y}'.format(\
               D= Day[weekday(LT[0],LT[1],LT[2])], M= Mon[LT[1]-1], d= LT[2],\
               h= LT[3], m= LT[4], s= LT[5], Y= LT[0] )

    # ------------------------------- Method -------------------------------- #
    @staticmethod
    def dayStamp():
        """
        Function returning a daystamp (string) in the format:
                         Wed_17_Jun_year
        """
        LT = localtime() # Timestamp information for filename
        Day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        Mon = ['Jan','Feb','Mar','Apr','May','Jun',\
               'Jul','Aug','Sep','Oct','Nov','Dec']
        return '{D}_{Num}_{M}_{Y}'.format(\
               D= Day[weekday(LT[0],LT[1],LT[2])], M= Mon[LT[1]-1], Num= LT[2],\
               Y= LT[0] )


