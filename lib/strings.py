__project_name__ = 'MeteoCom'
__program_version__ = 'v.1.1'


cli_divider = ':'
address_divider = ':'

default_map_path = './result-map.json'
default_tasks_path = './example-tasks+server.json'


class Console:
    program_start = f'Program {__project_name__} {__program_version__} started.'
    program_mode_parser = 'Program mode "parser" selected, starting..'
    example_parser_args_headers = f'<PORT>{cli_divider}<SLAVE_ADDR>{cli_divider}<RATE>{cli_divider}<NAME>{cli_divider}<RESULT_MAP_PATH>'
    example_parser_args_vars = f'/dev/tty10{cli_divider}1{cli_divider}57600{cli_divider}device{cli_divider}./device_map.json'
