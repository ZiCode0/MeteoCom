import json
import os

from lib.mapping import schemas
from lib.mapping import file


class DeviceMapper:
    def __init__(self, file_path=None):
        """
        Device mapper class to build registry map for modbus device
        :type file_path: load device mapper json data if specified
        """
        self.map = {}
        self._data = None
        # load json map if specified
        if file_path:
            self.read(file_path=file_path)

    def add_map_record(self, address, function='default', read_type='default', key=None, description=None, active=None):
        rec = {'address': address,
               'read_type': read_type}
        if key:
            rec['key'] = key
        if description:
            rec['description'] = description
        if active:
            rec['active'] = active
        schemas.record_schema.validate(rec)  # validate record
        self.map['device_mapper']['data'].append(rec)

    def read_json(self, json_data: dict):
        self.map = json_data['device_mapper']

    def read(self, file_path):
        self._data = file.read(file_path)
        self.map = self._data['device_mapper']

    def get_map(self):
        return {'device_mapper': self.map}

    def export_json(self, file_path='./device-map.json', get_object=False) -> str:
        """
        Export device mapper json file
        :param file_path :type str: target file path to export
        :param get_object :type bool flag to return file object
        """
        # replace "dot" with absolute path > link with "cwd" folder
        if file_path.startswith('./'):
            cwd = os.getcwd()
            file_path = file_path.replace('.', cwd, 1)
        # if in-project folder file input > put in "cwd" folder
        if '/' not in file_path:
            cwd = os.getcwd()
            file_path = f'{cwd}/{file_path}'
        # dump device map
        json_map = json.dumps(self.map, indent=4)

        if get_object:
            return json_map
        else:
            # export to file
            with open(file_path, 'w') as f:
                f.write(json_map)
            return file_path
