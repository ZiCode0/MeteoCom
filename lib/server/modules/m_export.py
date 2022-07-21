import os.path

from fastapi import HTTPException, APIRouter
from starlette.responses import StreamingResponse

import lib

router = APIRouter(
    tags=["Export"],
    responses={404: {"description": "Not found"}},
)


@router.post("/export_tasks_json")
async def export_task_json(export_path: str, download: bool = False):
    """Export tasks to json file"""
    try:
        # call export function
        save_response = lib.m_tasker.export_json(get_object=download, file_path=export_path)
        # make stream download
        if download:
            download_file_name = os.path.basename(export_path)
            response = StreamingResponse(iter([save_response]), media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={download_file_name}"
            return response
        # return result save local path
        else:
            return save_response
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/export_device_map_json")
async def export_device_map_json(export_path: str, download: bool = False):
    """Export device map to json file"""
    try:
        # call export function
        save_response = lib.d_mapper.export_json(get_object=download, file_path=export_path)
        # make stream download
        if download:
            download_file_name = os.path.basename(export_path)
            response = StreamingResponse(iter([save_response]), media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={download_file_name}"
            return response
        # return result save local path
        else:
            return save_response
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
