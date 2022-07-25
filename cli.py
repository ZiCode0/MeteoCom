import time

from lib.modbus import mb_server
from lib.tasker import tasker
from lib.mapping import mapper
from lib.config import config
from lib.cli import app

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
        if item:  # Empty element
            if "=" in item:
                key, value = item.split("=", maxsplit=1)
                kw_args[key] = value
    return kw_args


if __name__ == '__main__':
    # ####################### #
    # EXAMPLE CLI APP VERSION #
    # ####################### #
    ca = app.ConsoleApp()
    # dict_args = simple_input_parser(sys.argv[1:])
    dm = mapper.DeviceMapper()  # init device mapper instance
    dm.read(ca.args.map_path)  # read device mapper configs
    s = mb_server.MServer(port=target_port, rate=dm.map['info']['rate'], read_mode=dm.map['info']['protocol'],
                          slave_address=dm.map['info']['slave_address'], fake_connect=False)  # TODO: DEBUG
    t = tasker.Tasker(file_path=ca.args.task_path, modbus_server=s, device_mapper=dm)
    t.start()

    print('started')
    time.sleep(30)
    t.stop()
    print('stopped')
