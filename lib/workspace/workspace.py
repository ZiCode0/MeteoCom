import pandas as pd

from lib.config import config
from lib.workspace.export import export

conf = config.EnvConfig()


class Workspace:
    def __init__(self):
        self.buffer_size = conf.default.task_buffer_size
        self.report_sheet = conf.default.report_sheet
        self.dataframes = {}
        self.connections = {}
        self.backup_connection = None

    def add_dataframe(self, name: str, initial_data_array: list):
        """
        Initialize task workspace buffer dataframe
        :param name:
        :param initial_data_array:
        :return:
        """
        self.dataframes[name] = pd.DataFrame(data=None, columns=initial_data_array)
        # set float format
        pd.set_option('display.precision', 2)
        pd.options.display.float_format = '{:,.2f}'.format

    def add_row(self, df_name: str, row_object: dict):
        """
        Add row to pd.dataframe instance
        :param df_name: target dataframe
        :param row_object: dictionary to add as row
        :return:
        """
        # make row object as pandas dataframe
        df = pd.DataFrame(row_object, index=[0])
        # append record to task dataframe
        self.dataframes[df_name] = self.dataframes[df_name].append(df, ignore_index=True)
        # if size is more than 5 rows
        if self.dataframes[df_name].shape[0] > self.buffer_size:
            # remove first element to make dataframe size equal to 5 records
            self.dataframes[df_name] = self.dataframes[df_name].iloc[1:]
            # print()  # enable for #debug

    def export_last_row(self, name: str, export_path, method: str):
        """
        Export data
        :param name: target dataframe name
        :param export_path: target export path to file
        :param method: result export format
        :return:
        """
        # get last row record object
        tail = self.dataframes[name].tail(1)
        # method: text
        if method == 'text':
            try:
                tail.to_csv(export_path, header=None, index=None, sep=' ', mode='a')
            except FileNotFoundError:
                tail.to_csv(export_path, header=None, index=None, sep=' ')

        # method: excel
        elif method == 'excel':
            sheet_name = self.report_sheet
            start_row = None
            # try to open Excel file by export_path
            try:
                with pd.ExcelWriter(export_path, engine="openpyxl", mode='a') as writer:
                    # get the last row in the existing Excel sheet
                    # if it was not specified explicitly
                    if start_row is None and sheet_name in writer.book.sheetnames:
                        start_row = writer.book[sheet_name].max_row
                    # set sheet dictionary
                    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
                    # append data to existing excel
                    tail.to_excel(writer, startrow=start_row, sheet_name=sheet_name, index=None, header=None)
            except FileNotFoundError:
                # write new Excel file
                tail.to_excel(export_path, index=None, sheet_name=sheet_name)

        # method: db
        elif method == 'db':
            # print()
            if name in self.connections:
                export.to_db(data=tail,
                             table_name=name,
                             engine=self.connections[name])
            else:
                self.connections[name] = export.to_db(data=tail,
                                                      table_name=name,
                                                      db_path=conf.get('DB_PATH'))

        # method: json
        # export for custom requests
        elif method == 'json':
            return tail.to_dict('records')[0]

    def export_json(self):
        result_dict = {key: value.to_dict() for (key, value) in self.dataframes.items()}

        return result_dict
