import os
from collections import namedtuple
from pprint import pprint
from dotenv import load_dotenv

Net = namedtuple('Net', 'allowed_hosts port')
Default = namedtuple('Default', 'export_time_format task_buffer_size report_sheet debug')
Args = namedtuple('Args', 'mode map tasks out_file target_tasks')


class EnvConfig:
    def __init__(self, path=None):
        """
        Get environment variables
        """
        if not path:
            # try default read
            try:
                load_dotenv('.env')
            except:
                load_dotenv('../.env')
        else:
            load_dotenv(path)

        self.net = Net(allowed_hosts=str(os.environ.get("MS_HOST", default="0.0.0.0")),
                       port=int(os.environ.get("MS_PORT", default=6383)))
        # set default env params
        self.default = Default(export_time_format=str(os.environ.get("EXPORT_TIME_FORMAT",
                                                                     default="%Y-%m-%d_%H:%M:%S")),
                               task_buffer_size=int(os.environ.get("TASK_BUFFER_SIZE",
                                                                   default=5)),
                               report_sheet=str(os.environ.get("REPORT_SHEET",
                                                               default="report")),
                               debug=bool(os.environ.get("DEBUG",
                                                         default=False)))

        # set cli args
        self.args = Args(mode=None, map=None, tasks=None, out_file=None, target_tasks=None)

    def print_params(self):
        params = [self.net, self.default]
        for param in params:
            pprint(param)

    @staticmethod
    def get(value_name):
        return os.environ.get(value_name)
