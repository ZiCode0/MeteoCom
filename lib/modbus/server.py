import minimalmodbus
import random


class MServer:
    def __init__(self, port: str, rate: int, read_mode: str, slaveaddress: int = 1,
                 extra_options: bool = True, fake_connect: bool = False, **kwargs):
        """
        Modbus mservice instance to read data
        :param port: specify tty port
        :param rate: read rate
        :param read_mode: "rtu" or "ascii"
        :param extra_options: apply extra mservice extra options
        :param fake_connect: toggle and make fake connection to device
        """
        self.locked = False  # locker toggle
        self.fake_connect = fake_connect
        r_mode = {'rtu': minimalmodbus.MODE_RTU,
                  'ascii': minimalmodbus.MODE_ASCII}
        # catch exceptions
        # from serial.serialutil import SerialException
        if not self.fake_connect:
            self.engine = minimalmodbus.Instrument(port, slaveaddress, mode=r_mode[read_mode], **kwargs)
            self.engine.serial.baudrate = rate
            if extra_options:
                self.engine.close_port_after_each_call = True
                self.engine.clear_buffers_before_each_transaction = True
                # print()

    @staticmethod
    def read_data_fake(read_type='default'):
        """
        Read data with fake values
        :param read_type:
        :return:
        """
        read_functions = {'default': random.randint(0, 1000),  # self.engine.read_register,
                          'float': random.uniform(-100.0, 100.0),  # self.engine.read_float,
                          'long': random.randint(0, 100000),  # self.engine.read_long,
                          'bit': random.randint(0, 1)  # self.engine.read_bit}
                          }
        return read_functions[read_type]

    def read_data(self, register, function=0x03, read_type='default'):
        """
        Read data from specified register
        :param register: register number
        :param function: function read number
        :param read_type: default/float/long/bit
        :return:
        """
        # if fake connection
        if self.fake_connect:
            # return fake data
            return self.read_data_fake(read_type)

        read_functions = {'default': self.engine.read_register,
                          'float': self.engine.read_float,
                          'long': self.engine.read_long,
                          'bit': self.engine.read_bit}
        return read_functions[read_type](register, functioncode=function)

    def write_data(self, register, new_value, function=16):
        # if fake connection
        if self.fake_connect:
            # make fake write data
            pass
        else:
            self.engine.write_register(registeraddress=register,
                                       value=new_value,
                                       functioncode=function)
