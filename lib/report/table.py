from prettytable import PrettyTable

skip_field = ['...'] * 7


class ReportTable:
    def __init__(self, device_name, data):
        """
        Report table of device modbus map to output
        """
        # table params
        self.table_title = f'Device {device_name} registry map:'
        self.table = PrettyTable()
        self.table.field_names = ['addr(int)',
                                  'addr(hex)',
                                  'function',
                                  'val register',
                                  'val float',
                                  'val long',
                                  'val bit']
        self.data = data
        self.add_records(data)

    def add_records(self, records):
        self.table.add_rows(records)

    def print(self):
        print(self.table.get_string(title=self.table_title))

    def export(self, exclude_column: int):
        table = self.data
        # exclude element from sub lists by index
        for sub_list in table:
            del sub_list[exclude_column]
        # remove dot
        table = self.remove_dot_separator(data_array=table)
        return table

    @staticmethod
    def remove_dot_separator(data_array):
        """
        Fill data field
        :param data_array:
        :return:
        """
        new = []
        for dat in data_array:
            if '...' not in dat:
                new.append(dat)
        return new
