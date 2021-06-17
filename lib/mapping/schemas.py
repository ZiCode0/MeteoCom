from schema import Schema, And, Or, Optional, SchemaError

from lib.mapping.address import check_address

command_int_limit = 10
record_schema = Schema({  # 'address': And(int),
    # 'function': Or(lambda s: check_function_key(s)),
    'address': And(str, lambda s: check_address(s)),
    'read_type': And(str, lambda s: check_result_key(s)),
    # Optional('key'): And(str),
    Optional('description'): And(str),
    Optional('write'): And(hex, int)
    # Optional('active'): And(True)
})

header_schema = Schema({'device_name': And(str),
                        'protocol': And(str),
                        'rate': And(int)
                        })

config_schema = Schema({'device_mapper': {'info': header_schema,
                                          'data': And(lambda s: check_data_list(s))}
                        })

one_task_schema = Schema({'report_name': And(str),
                          'report_type': And(str, lambda s: check_report_type(s)),
                          'report_line': And(str),
                          Optional('repeat_timer'): And(lambda s: check_repeat_type(s))
                          })

tasks_schema = Schema({'tasks': And(dict, lambda s: check_tasks(s))})


def check_function_key(inp_key):
    """
    Function key checker
    :param inp_key: target key
    :return: bool
    """
    return inp_key in [  # 'default',  # default value
        *list(range(0, command_int_limit + 1))  # range function keys (0..10)
    ]


def check_result_key(inp_key):
    """
    Result key checker
    :param inp_key: target key
    :return: bool
    """
    return inp_key in ['default', 'float', 'int', 'bit']


def check_data_list(data):
    """
    Check input data records
    :param data:
    :return: bool
    """
    try:
        for key in data:
            # print()  # enable for #debug
            record_schema.validate(data[key])
        return True
    except SchemaError:
        return False


def check_report_type(report_type):
    return report_type in ['text', 'excel', 'console', 'db', 'json']


def check_tasks(tasks):
    """
    Validate task list
    :param tasks:
    :return:
    """
    for key in tasks:
        res = one_task_schema.validate(tasks[key])
        # print(res)  # enable for #debug
    return True


def check_repeat_type(repeat_type):
    if (repeat_type is False) or (type(repeat_type) is int):
        return True
