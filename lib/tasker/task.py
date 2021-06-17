import random
import datetime
import time
from pathlib import Path

from lib.tasker import task_line
from lib.config import config

conf = config.EnvConfig()

'''
TASK EXAMPLE:
    {"task_type": "read",
    "task_line": "{datetime} {temp1} {temp2} {press1} {press2}",
    "task_repeat": 2,
    "report_name": "{device_name}_{datetime}",
    "report_path": "default",
    "report_type": "text"}
'''


def get_set_data(args, modbus_server, device_mapper):
    """
    Once task function
    :param device_mapper:
    :param args:
    :param modbus_server:
    :return:
    """
    # prepare data
    targets = task_line.prepare(target_line=args['task_line'],
                                task_type=args['task_type'],
                                device_mapper=device_mapper)

    # task body
    def read_body():
        result_dict = {}
        # parse all task targets
        for name in targets:
            # skip datetime arg
            if name == 'datetime':
                # add datetime field for task in text format
                result_dict[name] = datetime.datetime.now().strftime(conf.default.export_time_format)
                # print()
            else:
                # call read function
                result_dict[name] = modbus_server.read_data(register=targets[name]['register'],
                                                            function=targets[name]['function'],
                                                            read_type=targets[name]['read_type'])
        # print()  # enable for #debug
        return result_dict

    def write_body():
        write_args, read_args = targets
        result_dict = {}
        # parse all task targets
        for name in write_args:
            # print()
            # call write function
            if 'write_function' not in read_args[name]:
                read_args[name]['write_function'] = 16
            result_dict[name] = modbus_server.write_data(register=read_args[name]['register'],
                                                         new_value=int(write_args[name]),
                                                         function=read_args[name]['write_function']
                                                         )
            # print()  # enable for #debug
        return result_dict

    # select task function by task_type
    task_body_dict = {'read': read_body,
                      'write': write_body}
    target_func = task_body_dict[args['task_type']]

    # main body of read/write data
    try:
        result = target_func()
        return result
    except Exception as ex:
        print(f'[!] Error in task: <{ex}>, repeat..')
        # exception try loop
        # try with sleep timer while success
        while True:
            try:
                time.sleep(random.uniform(0.01, 0.5))  # random wait on exception to pause
                result = target_func()
                return result
            except:
                continue


def make_export_path(task_args: dict,
                     d_mapper):
    """
    Make export path using task parameters
    :param task_args: task arguments dictionary
    :param d_mapper: Device mapper instance
    :return:
    """
    export_path = {}
    # prepare export path
    if task_args['report_path'] == 'default':
        export_path['report_path'] = Path('./')  # change path to default value
    else:
        export_path['report_path'] = Path(task_args['report_path'])

    # prepare export file name
    report_keys = task_line.parse_read_line(task_args['report_name'])
    for name in report_keys:
        if name == 'datetime':
            report_keys[name] = datetime.datetime.now().strftime(conf.default.export_time_format)
        elif name == 'device_name':
            report_keys[name] = d_mapper.map['info']['device_name']
    export_path['report_name'] = task_args['report_name'].format(**report_keys)

    # prepare export file extension (.txt, .xlsx)
    if task_args['report_type'] in ['text', 'txt']:
        export_path['report_type'] = '.txt'
    elif task_args['report_type'] in ['excel', 'xls', 'xlsx']:
        export_path['report_type'] = '.xlsx'

    # form result export file Path
    result_path: Path = export_path['report_path'] / (export_path['report_name'] + export_path['report_type'])
    return result_path
