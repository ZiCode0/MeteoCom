import json
import schema

from lib.mapping import schemas
from lib.mapping import address


def read(file_path):
    """
    Reading device mapper configs
    :return:
    """
    config_file = open(file_path, 'r')
    config_file = json.load(config_file)
    # print()  # enable for #debug
    return config_file


def dump_map(header, data, out_file=None, empty_field=''):
    """
    Dump device mapper data to json configs
    :return:
    """
    # init result map dict instance
    result_map = {'info': {'device_name': header[0],
                           'protocol': header[1],
                           'slave_address': int(header[2]),
                           'rate': int(header[3])},
                  'data': {}}
    counter = 1
    for record in data:
        # create register name
        res_register = address.set_address_name(register=record[0], function=record[1])
        # create record
        res_record = {  # 'address': record[0],
            # 'function': record[1],
            'address': res_register,
            'read_type': 'default'}
        # add register read record
        result_map['data'][str(counter)] = res_record  # .append(res_record)
        counter += 1

    # make configs head
    result_map = {'device_mapper': result_map}

    # try validate result output
    try:
        # validate output
        schemas.config_schema.validate(result_map)
        # dump data to json
        json_res = json.dumps(result_map, indent=4)

        # if out file path specified
        if out_file:
            open(out_file, '+w').write(json_res)
        # set default out file path
        else:
            # file path
            out_file = './' + result_map['device_mapper']['info']['device_name']
            # write
            open(out_file, '+w').write(json_res)
    except schema.SchemaError as ex:
        print(ex)
    # print()  # enable for #debug
