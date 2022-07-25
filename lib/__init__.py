from typing import Union

import loguru

from lib import strings
from lib.modbus import mb_server as ms
from lib.tasker import tasker as tsk
from lib.mapping import mapper
from lib.server import web_server as ws
from lib.workspace import workspace as wks

import lib.logger.logger as logger_lib

# init logger
logger_lib.init_logger(strings.__project_name__)

logger = loguru.logger
m_server: ms.MServer
m_tasker = Union[tsk.Tasker, None]  # None  # tsk.Tasker  # tasker.Tasker
# m_tasker_started = False
d_mapper = Union[mapper.DeviceMapper, None]  # mapper.DeviceMapper
workspace = Union[wks.Workspace, None]  # wks.Workspace

web_server: Union[ws.CWebServer, None] = None


def start_web_server():
    global web_server
    web_server = ws.CWebServer()
    web_server.start()


def stop_web_server():
    global web_server
    if web_server:
        web_server.stop()


def init_vars(i_m_server=None, i_m_tasker=None, i_d_mapper=None, i_w_server=None, i_logger=None, i_workspace=None):
    global m_server, m_tasker, d_mapper, web_server, logger, workspace
    if i_m_server:
        m_server = i_m_server
    if i_m_tasker:
        m_tasker = i_m_tasker
    if i_d_mapper:
        d_mapper = i_d_mapper
    if i_w_server:
        web_server = i_w_server
    if i_logger:
        logger = i_logger
    if i_workspace:
        workspace = i_workspace
