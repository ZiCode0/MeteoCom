import time
from lib.modbus.mb_server import MServer

usb_port = '/dev/ttyUSB1'
speed = 19200


s = MServer(debug=True, port=usb_port, rate=speed, read_mode='rtu')

while True:
    try:
        data = s.read_data(register=1)
        print(f'{s}')
    except Exception as ex:
        print(ex)
    time.sleep(3)
