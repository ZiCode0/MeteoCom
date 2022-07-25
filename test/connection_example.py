from lib.modbus.mb_server import MServer

ms = MServer(port='/dev/ttyUSB0', rate=19200, read_mode='rtu', slave_address=48, async_mode=True)

try:
    res = ms.read_data(6, read_type='default')
except Exception as ex:
    res = ex

print(f'{res}')
