from loguru import logger

import lib
from lib import strings
from lib.modbus import mb_server
from lib.tasker import tasker
from lib.mapping import mapper
from lib.config import config
from lib.cli import app as c_app
from lib.parser import rtu_parser

conf = config.EnvConfig()


@logger.catch
def main():
    # global m_server, m_tasker, d_mapper, m_tasker_started
    logger.info(strings.Console.program_start)
    # init console instance
    ca = c_app.ConsoleApp()
    # check and rewrite default values
    if not ca.args.port:
        ca.args.port = conf.default.device_port
    if not ca.args.task_path:
        ca.args.task_path = conf.args.task_path
    if not ca.args.map_path:
        ca.args.map_path = conf.args.map_path

    # check and start rtu_parser mode
    if ca.args.parser:
        logger.info(strings.Console.program_mode_parser)
        rtu_parser.run(args_str=ca.args.parser, logger=logger)

    # start : normal mode
    elif not ca.args.server:
        # start program
        d_mapper = mapper.DeviceMapper(ca.args.map_path)  # read device mapper configs
        m_server = mb_server.MServer(port=ca.args.port,
                                     rate=d_mapper.map['info']['rate'],
                                     read_mode=d_mapper.map['info']['protocol'],
                                     slave_address=d_mapper.map['info']['slave_address'],
                                     async_mode=True,
                                     fake_connect=conf.default.debug,
                                     logger=logger)

        # start tasks
        m_tasker = tasker.Tasker(file_path=ca.args.task_path,
                                 modbus_server=m_server,
                                 device_mapper=d_mapper,
                                 logger=logger)
        m_tasker.start()

        # lib.m_tasker_started = True
        lib.init_vars(i_m_server=m_server, i_m_tasker=m_tasker,
                      i_d_mapper=d_mapper)

        # check start server task
        if lib.m_tasker.server_mode:
            lib.start_web_server()

    # start : only server mode
    else:
        lib.start_web_server()

    while True:
        continue


if __name__ == '__main__':
    try:
        main()
    # make stop processes
    finally:
        # stop web server process
        lib.stop_web_server()
