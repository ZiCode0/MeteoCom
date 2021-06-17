import sys

from lib.modbus.server import MServer
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


def rtu_parser(port=PORT,
               rate=RATE,
               out_path=DEFAULT_PATH,
               device_name=DEVICE_NAME,
               read_functions=None,
               read_mode='rtu',
               **kwargs):
    """
    Modbus parser to build device map
    :param port: target device connection port
    :param rate: target device connection rate
    :param out_path: result output file with json device map
    :param device_name: device name for map
    :param read_functions: list of read functions
    :param read_mode: modbus mode "rtu"(default)/"ascii"
    :param kwargs: extra arguments for modbus server
    :return: result map view on screen, json out_path map
    """
    # Set up instrument
    if read_functions is None:
        read_functions = READ_FUNCTIONS
    if out_path is None:
        out_path = DEFAULT_PATH

    s = MServer(port, rate, read_mode=read_mode, **kwargs)  # init modbus server instance

    # parse registers
    table_buffer = []
    for func in read_functions:
        for index in range(index_max+1):
            try:
                try:
                    ss_reg = s.engine.read_register(index, functioncode=func)
                except:
                    ss_reg = ''
                try:
                    ss_flt = s.engine.read_float(index, functioncode=func, number_of_registers=2)
                except:
                    ss_flt = ''
                try:
                    ss_lng = s.engine.read_long(index, functioncode=func)
                except:
                    ss_lng = ''
                try:
                    ss_bit = s.engine.read_bit(index, functioncode=func)
                except:
                    ss_bit = ''

                if skip_empty:
                    if ss_reg == '' and ss_flt == '' and ss_lng == '' and ss_bit == '':
                        continue

                if type(ss_flt) == float:
                    ss_flt = f'{ss_flt:.2f}'
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

    # add header for json config dump
    header = [device_name, 'rtu', rate]
    # dump to json
    file.dump_map(header=header, data=table_buffer, out_file=out_path)

    assert file.read(file_path=out_path) is not None, False
    # print('debug')  # enable for #debug


if __name__ == '__main__':
    # sys.args
    rtu_parser(port=sys.argv[1],
               rate=int(sys.argv[2]),
               device_name=sys.argv[3],
               out_path=sys.argv[4])
