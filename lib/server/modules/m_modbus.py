from typing import Union
from fastapi import HTTPException, APIRouter

import lib
from lib.modbus.mb_server import MServer
from lib.server.models import ModbusServer, EmptyObject

router = APIRouter(
    tags=["Modbus"],
    responses={404: {"description": "Not found"}},
)


@router.get("/modbus", response_model=Union[ModbusServer, EmptyObject])
async def get_modbus_server():
    """Get modbus server status"""
    try:
        # if modbus server instance  not initialized
        if not lib.m_server:
            return EmptyObject()
        # if modbus server exists
        else:
            model = ModbusServer(port=lib.m_server.port,
                                 rate=lib.m_server.rate,
                                 read_mode=lib.m_server.read_mode,
                                 slave_address=lib.m_server.slave_address,
                                 fake_connect=lib.m_server.fake_connect)
            return model
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/modbus")
async def create_modbus_server(ims: ModbusServer):
    """Create modbus server instance"""
    try:
        # get logger instance
        m_server_logger = lib.logger
        # recreate MServer
        lib.m_server = MServer(logger=m_server_logger, **ims.dict())
        # set module var
        # lib.msm = ims
        return await get_modbus_server()  # ims  # lib.msm
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.put("/modbus")
async def modify_modbus_server(update_model: ModbusServer):
    """Modify modbus server var. * Re-init full instance"""
    try:
        m_server_logger = lib.logger
        # get current model
        current_model = await get_modbus_server()
        # get update model vars dict
        update_model_dict = update_model.dict(exclude_unset=True)
        # new model vars dict
        new_model = current_model.copy(update=update_model_dict)
        # set new m_server instance
        lib.m_server = MServer(logger=m_server_logger, **new_model.dict())

        # lib.msm = new_model
        return await get_modbus_server()  # lib.msm
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.delete("/modbus")
async def delete_modbus_server():
    """Delete modbus server var"""
    try:
        lib.m_server = None
        return await get_modbus_server()
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
