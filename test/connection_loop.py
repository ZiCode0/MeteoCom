import datetime
import time

from lib.modbus.mb_server import MServer

usb_port = '/dev/ttyUSB0'
speed = 19200
slave_address = 48
register = 8


while True:
    data = None
    # init server instances
    server = MServer(port=usb_port, rate=speed, read_mode='rtu', slave_address=slave_address)
    # try to fetch data
    try:
        data = server.read_data(register=register)
    except Exception as ex:
        data = ex
    # output data
    print(f'{datetime.datetime.now()}\tdata={data}')
    time.sleep(1)
