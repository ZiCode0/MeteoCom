import asyncio
import datetime
import time

# from parser import expr

from lib.modbus.mb_server import MServer

loop = asyncio.get_event_loop()

usb_port = '/dev/ttyUSB0'
speed = 19200
slave_address = 48
register = 8


while True:
    data, data_async = None, None
    # init server instances
    server = MServer(port=usb_port, rate=speed, read_mode='rtu', slave_address=slave_address)
    server_async = MServer(port=usb_port, rate=speed, read_mode='rtu', slave_address=slave_address, async_mode=True)
    # try to fetch data
    try:
        data = server.read_data(register=register)
    except Exception as ex:
        data = ex
    try:
        data_async = server_async.read_data(register=register)
    except Exception as ex:
        data_async = ex
    # output data
    print(f'{datetime.datetime.now()}\tsync={data}\tasync={data_async}')
    time.sleep(1)
