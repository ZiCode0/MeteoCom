import sys
import time

from lib.modbus import server
from lib.tasker import tasker
from lib.mapping import mapper
from lib.config import config

conf = config.EnvConfig()

target_port = '/dev/ttyUSB0'  # target device port


def simple_input_parser(input_args):
    """
    Parse sys.argv as dict
    :param input_args: target input args list
    :return: dict
    """
    kw_args = {}
    for item in input_args:
        item = item.rstrip(',')
        if item:  # Пустой элемент, например если была одиночная запятая
            if "=" in item:
                key, value = item.split("=", maxsplit=1)
                kw_args[key] = value
    return kw_args


if __name__ == '__main__':

    # ####################### #
    # EXAMPLE CLI APP VERSION #
    # ####################### #

    args, kwargs = simple_input_parser(sys.argv[1:])
    dm = mapper.DeviceMapper()  # init device mapper instance
    dm.read(args[0])  # read device mapper config
    s = server.MServer(port=target_port,
                       rate=dm.map['info']['rate'],
                       read_mode=dm.map['info']['protocol'],
                       fake_connect=True)
    t = tasker.Tasker(file_path=args[1], modbus_server=s, device_mapper=dm)
    # print()
    t.start()
    print('started')

    time.sleep(40)
    print(f'manual: {s.read_data(register=3)}')
    time.sleep(500)
