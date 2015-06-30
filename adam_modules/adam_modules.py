# -*- coding: ascii -*-
"""

oooooooooooo       oooo oooo                    ooooo                 .o8
`888'     `8       `888 `888                    `888'                "888
 888       .ooooo.  888  888  .ooooo.  .oooo.o   888         .oooo.   888oooo.
 888oooo8 d88' `88b 888  888 d88' `88bd88(  "8   888        `P  )88b  d88' `88b
 888    " 888ooo888 888  888 888ooo888`"Y88b.    888         .oP"888  888   888
 888      888    .o 888  888 888    .oo.  )88b   888       od8(  888  888   888
o888o     `Y8bod8P'o888oo888o`Y8bod8P'8""888P'  o888ooooood8`Y888""8o `Y8bod8P'


@summary:      Module for setting up a Modbus communication with minimalmodbus 
               to Adam-4000 and Adam-4100 modules
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

__author__  = "Sigve Karolius"
__email__   = "<firstname>ka<at>ntnu<dot>no"
__license__ = "GPL.v3"

#__revision__  = "$Rev: 155 $"
__date__      = "$Date: 2015-06-23 (Tue, 23 Jun 2015) $"

from minimalmodbus import Instrument
# 'read_bit', 'read_float', 'read_long', 'read_register', 'read_registers', 'read_string', 'write_bit', 'write_float', 'write_long', 'write_register', 'write_registers', 'write_string'

class DummySerial(object):
    def flushOutput(self):
        pass
    def flushInput(self):
        pass
    def write(self, message):
        pass
    def read(self):
        return b'Blaah'

class DummyModbus(object):
    def __init__(self, portname, slaveaddress):
        self.serial = DummySerial()
    def read_register(self, channel):
        return None
    def read_registers(self, channel, number_of_channels):
        return list()
    def write_register(self, channel, value):
        pass
    def write_bit(self, channel, value):
        pass
    def read_bit(self, channel):
        return None



USE_DUMMY_MODBUS = False

if USE_DUMMY_MODBUS:
    minimalmodbus.Instrument = DummyModbus

class input:
    pass

class output:
    pass

# instrument.serial.port          # this is the serial port name
# instrument.serial.baudrate = 19200   # Baud
# instrument.serial.bytesize = 8
# instrument.serial.parity   = serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.timeout  = 0.05   # seconds
# 
# instrument.address     # this is the slave address number
# instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

# ================================= Class ==================================== #
class AdamModule(Instrument):
    """
    Parent class for ADAM modules
    
    Args:
         * portname (string, e.g. '/dev/ttyUSB1'): port name 
         * slaveaddress (integer): slave address in the range 1 to 247
    """
# 'read_bit', 'read_float', 'read_long', 'read_register', 'read_registers', 'read_string', 'write_bit', 'write_float', 'write_long', 'write_register', 'write_registers', 'write_string'

    def __init__(self, child=None, *args, **kwargs):
        """
        Constructor
        """
        if not kwargs.has_key('portname'):
            try:
                # search for port 
                pass
            except:
                Exception("Signal portname on the ADAM module is missing")

        if not kwargs.has_key('slaveaddress'):
            Exception("Missing ADAM module's address")
        
        Instrument.__init__(self, *args, **kwargs)

    def module_name(self):
        """
        Read name from module
        """
        return self.read_register(210) # child.moduleName

    def module_version(self):
        """
            Read module version
        """
        return self.read_register(212) # child.moduleVersion

    def is_correct_module(self):
        """
            Check if the module class is correct 
        """
        if self.name == self.module_name(): # 
            return True
        else:
            return False

    def is_valid_channel(self, channel, number_of_channels):
        """
            Check if channel is valid
        """
        try:
            int(channel)
        except ValueError:
            print('Channel input not an integer')
            return False

        if channel >= 0 and channel <= number_of_channels:
            return True
        else:
            print('Channel input outside available channels: [0, ' + str(number_of_channels) + ']')
            return False

# ================================= Class ==================================== #
class AnalogIn(AdamModule):
    """
        Class for analog input ADAM modules
    """
    def __init__(self, *args, **kwargs):   
        """
            Constructor
        """ 
        AdamModule.__init__(self, *args, **kwargs)

    def get_analog_in(self, channel=-1):
        """
            Getter method
        """
        if channel == -1:
            return self.read_registers(self.analog_in_start_channel - 1, self.analog_in_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_in_number_of_channels):
            return self.read_register(self.analog_in_start_channel - 1 + channel)
        else:
            print('Channel out of range')
        
    def set_type_analog_in(self, channel, value):
        """
            Setter method
        """
        return self.write_register(self.type_analog_in_start_channel - 1 + channel, value)

    def get_type_analog_in(self, channel=-1):
        """
            Getter method
        """
        if channel == -1:
            return self.read_registers(self.type_analog_in_start_channel - 1, self.analog_in_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_in_number_of_channels):
            return self.read_register(self.type_analog_in_start_channel - 1 + channel)
        else:
            print('Channel out of range')

    def get_burn_out_signal(self, channel):
        """
            Burn signal
        """
        return self.read_bit(self.burn_out_signal_start_channel - 1 + channel)

# ================================= Class ==================================== #
class AnalogOut(AdamModule):
    analog_out_start_channel = 1
    type_analog_out_start_channel = 201
    analog_out_number_of_channels = 8

    def set_analog_out(self, channel, value):
        """
            Setter
        """
        return self.write_register(self.analog_out_start_channel - 1 + channel, value)

    def get_analog_out(self, channel=-1):
        """
            Getter
        """
        if channel == -1:
            return self.read_registers(self.analog_out_start_channel - 1, self.analog_out_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_out_number_of_channels):
            return self.read_register(self.analog_out_start_channel - 1 + channel)
        else:
            print('Channel out of range')

    def set_type_analog_out(self, channel, value):
        """
            Setter
        """
        return self.read_register(self.analog_out_start_channel - 1 + channel, value)

    def get_type_analog_out(self, channel=False):
        """
            Getter
        """
        if channel == -1:
            return self.read_registers(self.analog_out_start_channel - 1, self.analog_out_number_of_channels)
        elif self.is_valid_channel(channel, self.analog_out_number_of_channels):
            return self.read_register(self.analog_out_start_channel - 1 + channel)
        else:
            print('Channel out of range')

# ================================= Class ==================================== #
class DigitalIn(AdamModule):
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8

    def get_digital_in(self, channel):
        """
            Getter
        """
        return self.read_bit(self.diginal_in_start_channel - 1 + channel)

# ================================= Class ==================================== #
class DigitalOut(AdamModule):
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8

    def set_digital_out(self, channel, value):
        """
            Setter
        """
        return self.write_bit(self.digital_out_start_channel - 1 + channel, value)

    def get_digital_out(self, channel):
        """
            Getter
        """
        return self.read_bit(self.digital_out_start_channel - 1 + channel)

# ================================= Class ==================================== #
class Adam4117(AnalogIn):
    """
    Adam-4117
    """
    name = 16663
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 1
    analog_in_number_of_channels = 8

    # Type       Code
    # +/- 100mV: 2
    # +/-500 mV: 3
    # +/-1V:     4
    # +/- 2,5V:  5
    # 4~20mA:    7
    # +/-10V:    8
    # +/-5V:     9
    # 0~20 mA:   13
    # K:         15
    # T:         16
    # E:         17
    # R:         18
    # S:         19
    # B:         20
    # J:         14

# ================================= Class ==================================== #
class Adam4019(AnalogIn):
    """
        ADAM4019 sugar class
    """

    # ---------------------------- Method ------------------------------------ #
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """

#            analog_in_start_channel = 1,
#            type_analog_in_start_channel = 201,
#            burn_out_signal_start_channel = 1,
#            analog_in_number_of_channels = 8

        AnalogIn.__init__(self, *args, **kwargs)


# ================================= Class ==================================== #
class Adam4024(AnalogOut, DigitalIn):
    """
    ADAM4024
    """
    name = None
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 201
    analog_in_number_of_channels = 4
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 4

    # Analog out signal range is 0 to 409[5 or 6]
    # should scale such that value goes from 0 to 1

    # Types
    # 48: 0~20 mA
    # 49: +/- 10V
    # 50: 4~20 mA

# ================================= Class ==================================== #
class Adam4055(DigitalIn, DigitalOut):
    """
    ADAM4055
    """
    name = None
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8

# ================================= Class ==================================== #
class Adam4069(DigitalOut):
    """
    ADAM4069
    """
    name = None
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8