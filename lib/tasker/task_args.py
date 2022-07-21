from string import Formatter


def split_address(target_address):
    """
    Split mapper address by rule: addr('1:2') => function(addr[0]), register(addr[1])
    :param target_address:
    :return:
    """
    sp = target_address.split(':')
    return {'function': int(sp[0]), 'register': int(sp[1])}


def parse_read_line(target_line: str, return_format='dict'):
    """
    Prepare task read line. Convert string to dictionary
    :param return_format: result return format <'dict'/'list'>
    :param target_line: target line for parsing to dict form
    :return: dictionary
    """
    if return_format == 'dict':
        return {f_name: None for _, f_name, _, _ in Formatter().parse(target_line) if f_name}
    elif return_format == 'list':
        return [f_name for _, f_name, _, _ in Formatter().parse(target_line) if f_name]


def parse_write_line(target_line: str):
    """
   Prepare task write line. Convert string to dictionary
   :param target_line: target line for parsing to dict form
   :return: dictionary
   """
    write_targets = {}
    target_conditions = target_line.split()
    for target in target_conditions:
        part_key = parse_read_line(target, return_format='list')
        part_val = target.split('=')[1]
        for key in part_key:
            write_targets.update({key: part_val})
    return write_targets


def prepare(target_line, device_mapper, task_type):
    """
    Parse format input arguments of task line and prepare task
    :param device_mapper: add device mapper to find keys
    :param target_line:
    :param task_type: type of task line text (read/write)
    """
    # on "read" task type
    if task_type == 'read':
        args = parse_read_line(target_line)
        # parse equal keys to fill task parameters
        for dm_key in device_mapper.map['data']:
            for arg in args:
                if dm_key == arg:
                    # fill rules from mapper dictionary
                    args[arg] = device_mapper.map['data'][dm_key]
                    # split address => read_function:register
                    split_addr = split_address(args[arg]['address'])
                    # update task map dictionary
                    args[arg].update(split_addr)
                else:
                    # remove undefined param
                    pass
                    # del args[arg]
        # print()  # enable for #debug
        return args

    # on "write" task type
    elif task_type == 'write':
        # args = parse_read_line(target_line)
        write_args = parse_write_line(target_line)
        read_args = {}
        # parse equal keys to fill task parameters
        for dm_key in device_mapper.map['data']:
            for arg in write_args:
                if dm_key == arg:
                    # fill rules from mapper dictionary
                    read_args[arg] = device_mapper.map['data'][dm_key]
                    # split address => read_function:register
                    split_addr = split_address(read_args[arg]['address'])
                    # update task map dictionary
                    read_args[arg].update(split_addr)
                else:
                    # remove undefined param
                    pass
                    # del args[arg]

        # print()  # enable for #debug
        return write_args, read_args
    else:
        return None
