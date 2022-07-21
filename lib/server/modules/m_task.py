from typing import Union, List
from fastapi import HTTPException, APIRouter
from pydantic import parse_obj_as

import lib
import lib.tasker
from lib.server.models import Task, ResponseError, TaskUpdate
from lib.server.web_server import ErrorCreateObject

router = APIRouter(
    tags=["Task"],
    responses={404: {"description": "Not found"}},
)


@router.get("/task", response_model=Union[List[Task], Task, ResponseError], response_model_exclude_unset=True)
async def get_task(name: str = "all"):
    """Get task or tasks"""
    try:
        if not lib.m_tasker:
            raise lib.tasker.ExTaskerNotExist()
        # else
        if name == 'all':
            dict_tasks = lib.m_tasker.get_tasks_dict_as_list()
            model = parse_obj_as(List[Task], dict_tasks)
        else:
            model = parse_obj_as(Task, lib.m_tasker.get_tasks_dict()[name])
        return model
    # defined errors
    except lib.tasker.ExTaskerNotExist as ex:
        return ResponseError(code=ex.code, message=ex.message)
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/task")
async def create_task(i_model: Task):
    """Create task object"""
    if not lib.m_tasker:
        raise lib.tasker.ExTaskerNotExist()
    try:
        # send and add task to tasker
        response = lib.m_tasker.task_add(enabled=i_model.enabled,
                                         t_type=i_model.task_type,
                                         name=i_model.task_name,
                                         args=i_model.dict(),
                                         task_repeat=i_model.task_repeat)
        # task created
        if response:
            # get task object by name
            return await get_task(name=i_model.task_name)
        # task creation failed
        else:
            raise ErrorCreateObject("task", i_model.dict())
    # defined errors
    except lib.tasker.ExTaskerNotExist or ErrorCreateObject as ex:
        return ResponseError(code=ex.code, message=ex.message)
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.put("/task")
async def modify_task(update_model: TaskUpdate):
    """Edit task"""
    if not lib.m_tasker:
        raise lib.tasker.ExTaskerNotExist()
    try:
        # get current model
        current_model = await get_task(name=update_model.task_name)
        # get update model vars dict
        update_model_dict = update_model.dict(exclude_unset=True)
        # new model vars dict
        new_model = current_model.copy(update=update_model_dict)
        # stop task before edit
        if current_model.enabled:
            lib.m_tasker.task_stop(task_name=update_model.task_name)
        # recreate task
        await create_task(new_model)
        # get task instance
        return await get_task(name=update_model.task_name)

    # defined errors
    except lib.tasker.ExTaskerNotExist as ex:
        return ResponseError(code=ex.code, message=ex.message)
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.delete("/task")
async def delete_task(name: str):
    """Delete task"""
    try:
        lib.m_tasker.task_remove(task_name=name)
        return {'code': 200}
    # defined errors
    except lib.tasker.ExTaskObjectRemoveError or lib.tasker.ExTaskerNotEnabled or lib.tasker.ExTaskObjectNotFound as ex:
        return ResponseError(code=ex.code, message=ex.message)
    # return another errors
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
