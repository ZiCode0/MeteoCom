from typing import Union
from fastapi import HTTPException, APIRouter

import lib
from lib.server.models import TaskerOutput, TaskerInput, EmptyObject
from lib.tasker import tasker


router = APIRouter(
    tags=["Tasker"],
    responses={404: {"description": "Not found"}},
)


@router.get("/tasker", response_model=Union[TaskerOutput, EmptyObject])
async def get_tasker():
    """Get tasker status"""
    try:
        # if tasker instance  not initialized
        if not lib.m_tasker:
            return EmptyObject()
        # if tasker exists
        else:
            # if lib.m_tasker.self.
            model = TaskerOutput(enabled=lib.m_tasker.get_status(),
                                 task_count=lib.m_tasker.get_tasks_count(),
                                 tasks=lib.m_tasker.get_tasks_status_dict(),
                                 task_file_path=lib.m_tasker.get_task_file_path())
            return model
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/tasker")
async def create_tasker(i_model: TaskerInput):
    """Create tasker instance"""
    try:
        # get object instances
        m_server = lib.m_server
        m_server_logger = lib.logger
        d_mapper = lib.d_mapper
        # stop tasker
        # # check if tasker not DELETED
        if lib.m_tasker:
            # # tasker enabled
            if lib.m_tasker.enabled:
                lib.m_tasker.stop()
        # recreate Tasker
        lib.m_tasker = tasker.Tasker(file_path=i_model.task_file_path,
                                     modbus_server=m_server,
                                     device_mapper=d_mapper,
                                     logger=m_server_logger)
        # enable tasker by schemas
        if i_model.enabled:
            lib.m_tasker.start()
        # set module var
        return await get_tasker()  # ims  # lib.msm
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.put("/tasker")
async def modify_tasker(update_model: TaskerInput):
    """Modify tasker var. * Re-init full instance"""
    try:
        # get current model
        current_model = await get_tasker()
        # get update model vars dict
        update_model_dict = update_model.dict(exclude_unset=True)
        # new model vars dict
        new_model = current_model.copy(update=update_model_dict)
        # print()
        # set new m_tasker instance
        # # stop tasker
        if current_model.enabled:
            lib.m_tasker.stop()
        # # init tasker instance
        lib.m_tasker = tasker.Tasker(modbus_server=lib.m_server,
                                     device_mapper=lib.d_mapper,
                                     file_path=new_model.task_file_path,  # new
                                     logger=lib.logger)
        # enable on hot-plug if 'enabled' status in new model
        if new_model.enabled:
            lib.m_tasker.start()

        return await get_tasker()

    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.delete("/tasker")
async def delete_tasker():
    """Delete tasker var"""
    try:
        # stop tasker
        # # check if tasker not DELETED
        if lib.m_tasker:
            # # tasker enabled
            if lib.m_tasker.enabled:
                lib.m_tasker.stop()
        lib.m_tasker = None
        return await get_tasker()
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
