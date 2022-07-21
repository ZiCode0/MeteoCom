from typing import Union
from pydantic import parse_obj_as
from fastapi import HTTPException, APIRouter

import lib
from lib.mapping.mapper import DeviceMapper
from lib.server.models import DeviceMapper, EmptyObject

router = APIRouter(
    tags=["Mapper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/mapper", response_model=Union[DeviceMapper, EmptyObject], response_model_exclude_unset=True)
async def get_device_mapper():
    """Get device mapper"""
    try:
        if not lib.d_mapper:
            return EmptyObject()
        response_map = lib.d_mapper.get_map()
        model = parse_obj_as(DeviceMapper, response_map)
        return model
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.post("/mapper", response_model=DeviceMapper)
async def create_device_mapper(i_model: DeviceMapper):
    """Create device mapper"""
    try:
        # reinit device mapper
        lib.d_mapper = DeviceMapper()
        # load model dict
        lib.d_mapper.read_json(i_model.dict())
        return await get_device_mapper()
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))


@router.delete("/mapper")
async def create_device_mapper():
    """Delete device mapper"""
    try:
        # clear device mapper
        lib.d_mapper = None
        return await get_device_mapper()
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
