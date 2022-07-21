from fastapi import HTTPException, APIRouter

import lib
from lib.tasker import task

router = APIRouter(
    tags=["Data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/data")
async def get_data(register: str):
    """Get modbus register data"""
    try:
        # prepare input dictionary data
        i_args = {"task_type": "read",
                  "task_args": "{register}".replace("register", register)}
        # get data
        resp_data = task.get_set_data(args=i_args, once_fail_run=True,
                                      modbus_server=lib.m_server, device_mapper=lib.d_mapper, logger=lib.logger)
        return resp_data
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/data")
async def set_data(register: str, data: str):
    """Write data to modbus register"""
    try:
        # prepare input dictionary data
        i_args = {"task_type": "write",
                  "task_args": "{register}=value"
                  .replace("register", register)
                  .replace("value", data)
                  }
        # get data
        # TODO: fix get response data / None response - normal?
        resp_data = task.get_set_data(args=i_args, once_fail_run=True,
                                      modbus_server=lib.m_server, device_mapper=lib.d_mapper, logger=lib.logger)
        return resp_data
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
