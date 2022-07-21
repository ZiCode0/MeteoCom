import os
import sqlite3
from pathlib import Path


class BackupDefaultDriver:
    def __init__(self):
        # specify backup folder
        self.project_start_root_path = Path(__file__).parent.parent.parent
        self.project_backup_folder = self.project_start_root_path / 'backup'
        # specify backup file
        self.project_backup_file = self.project_backup_folder / '{datetime}-{backup_name}.txt'

    def check_empty(self):
        pass

    def put_data(self, data):
        """
        Save pandas dataframe data to csv
        :table_name: db table name to save data
        :param data: target data
        :return: bool Success
        """
        pass

    def get_data(self):
        """
        Get data as pandas dataframe
        :return:
        """
        pass

    def clear_all(self):
        pass


class BackupSqlDriver:
    def __init__(self, backup_folder=None, backup_file_name='backup.sql'):
        # specify backup folder
        # # based on project root folder
        if not backup_folder:
            self.project_start_root_path = Path(__file__).parent.parent.parent
            self.project_backup_folder = self.project_start_root_path / 'backup'
        # # based on input string path
        else:
            self.project_backup_folder = Path(backup_folder)

        # specify backup file
        self.project_backup_file = self.project_backup_folder / backup_file_name

        # make folder if not exist
        try:
            os.mkdir(self.project_backup_folder)
        except FileExistsError:
            pass

        # try to connect db
        self.conn = sqlite3.connect(self.project_backup_file)
        self.cur = self.conn.cursor()
        self.backup_empty = self.check_empty()
        print()

    def check_empty(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        exist = self.cur.fetchall()
        if exist:
            return True
        else:
            return False

    def put_data(self, data, table_name='default'):
        """
        Save pandas dataframe data to db
        :param data: target data
        :param table_name: db table name to save data
        :return: bool Success
        """
        pass

    def get_data(self):
        """
        Get data as pandas dataframe
        :return:
        """
        pass

    def clear_all(self):
        pass


if __name__ == '__main__':
    # bdr = BackupSqlDriver()
    print()
