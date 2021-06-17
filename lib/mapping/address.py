import re
from lib import strings

divider = strings.address_divider


def set_address_name(register, function):
    return f'{function}{divider}{register}'


def get_address_name(string):
    return string.split(divider)


def check_address(target_string):
    if re.match('^[0-9]+:[0-9]+$', target_string):
        return True
