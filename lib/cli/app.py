import argparse

from lib import strings


class ConsoleApp:
    def __init__(self):
        """
        Initial console app function
        """
        self.app_name = strings.__project_name__
        self.app_version = strings.__program_version__
        self.author = 'ZiCode0'
        self.contacts = '[Telegram] @MrFantomz'
        self.args = None

        # define program description
        text = '{app_name} by {author} v.{app_version}\nContacts: {contacts}'.format(app_name=self.app_name,
                                                                                     author=self.author,
                                                                                     app_version=self.app_version,
                                                                                     contacts=self.contacts)
        # initiate the parser with a description
        parser = argparse.ArgumentParser(description=text)
        parser.add_argument("-v", "--version", help="show program version", action="store_true")
        parser.add_argument("-p", "--port", help="modbus device port path", default="/dev/ttyUSB0")
        # map_path=PWS800-map.json task_path=PWS800-tasks+server.json
        parser.add_argument("-m", "--map_path", help="json device map file", default="map.json")
        parser.add_argument("-t", "--task_path", help="json device tasks file", default="tasks+server.json")
        parser.add_argument("-s", "--server", help="enable http server mode only", action="store_true")
        parser.add_argument("-P", "--parser", help="run parser to generate device map.\n" +
                                                   f"Example string ({strings.Console.example_parser_args_headers}):\n" +
                                                   f"{strings.Console.example_parser_args_vars}", default=None)

        self.args = parser.parse_args()
        if self.args.version:
            print(self.app_version)
            quit(0)
