import sys

from lib.modbus.mb_server import MServer
from lib.mapping import file
from lib.report import table
from lib import strings

PORT = '/dev/ttyUSB0'
DEVICE_NAME = 'default'  # read from cmd
DEFAULT_PATH = strings.default_map_path
RATE = 57600  # read from cmd
READ_FUNCTIONS = [1, 2, 3, 4, 5, 6]

index_max = 70  # register scan depth
skip_empty = True  # skip empty registers


def run(args_str: str, logger=None):
    """
    Run rtu parser from cli interface
    :param args_str: target parser string line
    :param logger: logger instance
    :return:
    """
    # parse args
    f_args = parse_args(args_string=args_str)
    # run parser
    rtu_parser_body(**f_args, logger=logger)
    # exit
    sys.exit(0)


def parse_args(args_string: str):
    """
    Parse rtu parser function target string
    Example string
        <PORT>:<RATE>:<NAME>:<RESULT_MAP_PATH>:
        /dev/tty10:57600:device:./device_map.json
    :param args_string: target args string
    :return: dict
    """
    args_string = args_string.split(strings.cli_divider)
    return {
        'port': args_string[0],
        'slave_address': int(args_string[1]),
        'rate': args_string[2],
        'device_name': args_string[3],
        'out_path': args_string[4]
    }


def rtu_parser_body(port: str = PORT,
                    slave_address: int = 1,
                    rate: int = RATE,
                    device_name: str = DEVICE_NAME,
                    out_path: str = DEFAULT_PATH,
                    read_functions=None,
                    read_mode='rtu',
                    logger=None,
                    **kwargs):
    """
    Modbus parser to build device map
    :param port: target device connection port
    :param slave_address: target slave address to connect device
    :param rate: target device connection rate
    :param device_name: device name for map
    :param out_path: result output file with json device map
    :param read_functions: list of read functions
    :param read_mode: modbus mode "rtu"(default)/"ascii"
    :param kwargs: extra arguments for modbus server
    :return: result map view on screen, json out_path map
    :param logger: logger instance
    """
    # Set up instrument
    if read_functions is None:
        read_functions = READ_FUNCTIONS
    if out_path is None:
        out_path = DEFAULT_PATH

    s = MServer(port, rate, read_mode=read_mode, slave_address=slave_address, logger=logger,
                **kwargs)  # init modbus server instance

    # parse registers
    table_buffer = []
    for func in read_functions:
        for index in range(index_max+1):
            try:
                try:
                    # sync: s.engine.read_register(index, functioncode=func)
                    ss_reg = s.read_data(index, function=func, read_type='default')
                except Exception as ex:
                    ss_reg = ''
                try:
                    # sync: s.engine.read_float(index, functioncode=func, number_of_registers=2)
                    ss_flt = s.read_data(index, function=func, read_type='float')
                except Exception as ex:
                    ss_flt = ''
                try:
                    # sync: s.engine.read_long(index, functioncode=func)
                    ss_lng = s.read_data(index, function=func, read_type='long')
                except Exception as ex:
                    ss_lng = ''
                try:
                    # sync: s.engine.read_bit(index, functioncode=func)
                    ss_bit = s.read_data(index, function=func, read_type='bit')
                except Exception as ex:
                    ss_bit = ''

                if skip_empty:
                    if ss_reg == '' and ss_flt == '' and ss_lng == '' and ss_bit == '':
                        continue

                if type(ss_flt) == float:
                    ss_flt = f'{ss_flt:.2f}'
                # debug
                # print(index, str(hex(index)), func, ss_reg, ss_flt, ss_lng, ss_bit)
                # add record to output table
                table_buffer.append([index, str(hex(index)), func, ss_reg, ss_flt, ss_lng, ss_bit])

            except Exception as ex:
                print(index, func, ex)
                continue

        # fill empty data with dot separator
        if func != read_functions[-1]:
            table_buffer.append(table.skip_field)

    # out result to console
    t = table.ReportTable(device_name, data=table_buffer)
    t.print()

    # prepare data to export
    table_buffer = t.export(exclude_column=1)  # remove_dot_separator(data_array=table_buffer)

    # add header for json configs dump
    header = [device_name, 'rtu', slave_address, rate]
    # dump to json
    file.dump_map(header=header, data=table_buffer, out_file=out_path)

    assert file.read(file_path=out_path) is not None, False
    # print('debug')  # enable for #debug


if __name__ == '__main__':
    # sys.args
    rtu_parser_body(port=sys.argv[1],
                    slave_address=int(sys.argv[2]),
                    rate=int(sys.argv[3]),
                    device_name=sys.argv[4],
                    out_path=sys.argv[5])
