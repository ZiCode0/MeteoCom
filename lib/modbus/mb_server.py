import time

from minimalmodbus import MODE_RTU, MODE_ASCII, NoResponseError
from asynciominimalmodbus import AsyncioInstrument
import random

import serial.serialutil


class MServer:
    def __init__(self, port: str, rate: int, read_mode: str, slave_address: int = 1,
                 extra_options: bool = True, logger=None, fake_connect: bool = False, **kwargs):
        """
        Modbus mservice instance to read data
        :param port: specify tty port
        :param rate: read rate
        :param read_mode: "rtu" or "ascii"
        :param extra_options: apply extra mservice extra options
        :param fake_connect: toggle and make fake connection to device
        :type logger: logger instance to output info
        """
        self.port = port
        self.rate = rate
        self.read_mode = read_mode
        self.slave_address = slave_address
        self.fake_connect = fake_connect

        self.wait_device_sec_timer = 5
        self.locked = False  # locker toggle
        self.logger = logger
        r_mode = {'rtu': MODE_RTU,
                  'ascii': MODE_ASCII}
        # catch exceptions
        # from serial.serialutil import SerialException
        if not self.fake_connect:
            def get_engine():
                try:
                    engine = AsyncioInstrument(port, slave_address, mode=r_mode[read_mode], **kwargs)
                    return engine
                except serial.serialutil.SerialException:
                    s_warning_conn_failed = f'Connection to device "{port}" failed. Waiting {self.wait_device_sec_timer} seconds..'
                    self.print_debug(s_warning_conn_failed, level='error')
                    # wait synchronous timer
                    time.sleep(self.wait_device_sec_timer)
                    return get_engine()

            self.engine = get_engine()
            self.engine.serial.baudrate = rate
            if extra_options:
                self.engine.close_port_after_each_call = True
                self.engine.clear_buffers_before_each_transaction = True
                # print()  # enable for #debug
        else:
            s_fake_conn_enabled = f'Fake debug connection to device: enabled'
            self.print_debug(s_fake_conn_enabled, level='warning')

    def print_debug(self, string: str, level='info'):
        """
        Print debugging information function using native print() or logger object
        :param string: target string to output
        :param level: debugger object level
        """
        if self.logger:
            if level == 'info':
                self.logger.info(string)
            elif level == 'warning':
                self.logger.warning(string)
            elif level == 'error':
                self.logger.error(string)
            else:
                Exception(f'Debug level {level} not found..')
        else:
            print(string)

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

        async def do():
            return await read_functions[read_type](register, functioncode=function)

        return do()

    def write_data(self, register, new_value, function=16):
        # if fake connection
        if self.fake_connect:
            # make fake write data
            pass
        # 'real' write register
        else:
            try:
                async def do():
                    response = await self.engine.write_register(registeraddress=register,
                                                                value=new_value,
                                                                functioncode=function)
                    return response
                return do()
            except NoResponseError:
                return None
