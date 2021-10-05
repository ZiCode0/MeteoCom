from lib.modbus.server import MServer

ms = MServer(port='/dev/ttyUSB0', rate=57600, read_mode='rtu')
data = ms.read_data(register=1)
