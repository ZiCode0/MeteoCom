import os
from collections import namedtuple
from distutils.util import strtobool
from pprint import pprint
from dotenv import load_dotenv

Net = namedtuple('Net', 'allowed_hosts port')
Default = namedtuple('Default', 'export_filename_time_format export_time_format task_buffer_size report_sheet debug')
Args = namedtuple('Args', 'device_port map_path task_path')
Routes = namedtuple('Routes', 'default status get cmd')


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

        self.routes = Routes(default='/',
                             status='/api/status',
                             get='/api/get/<string:target>',
                             cmd='/api/cmd/<string:target>')

        # set default env params
        self.default = Default(export_filename_time_format=str(os.environ.get("EXPORT_FILENAME_TIME_FORMAT",
                                                                              default="%Y-%m-%d")),
                               export_time_format=str(os.environ.get("EXPORT_TIME_FORMAT",
                                                                     default="%Y.%m.%d %H:%M:%S")),
                               task_buffer_size=int(os.environ.get("TASK_BUFFER_SIZE",
                                                                   default=5)),
                               report_sheet=str(os.environ.get("REPORT_SHEET",
                                                               default="report")),
                               debug=bool(strtobool(os.environ.get("DEBUG", default='False')))
                               )

        # set cli args
        self.args = Args(device_port=str(os.environ.get("PORT",
                                                        default="/dev/ttyUSB0")),
                         map_path=str(os.environ.get("MAP_PATH",
                                                     default="map.json")),
                         task_path=str(os.environ.get("TASKS_PATH",
                                                      default="tasks+server.json")),
                         )

    def print_params(self):
        params = [self.net, self.routes, self.default, self.args]
        str_buffer = []
        for param in params:
            str_buffer.append(param)
            pprint(param)
        return str_buffer

    @staticmethod
    def get(value_name):
        return os.environ.get(value_name)


class FlaskConfig(object):
    d_mapper = None
    d_tasker = None
    d_workspace = None
