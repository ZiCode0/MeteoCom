from lib.mapping import schemas
from lib.mapping import file


class DeviceMapper:
    def __init__(self):
        """
        Device mapper class to build registry map for modbus device
        """
        self.map = {}

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

    def read(self, file_path):
        self.map = file.read(file_path)['device_mapper']
