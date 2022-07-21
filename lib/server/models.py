from typing import Union, Dict

from pydantic import BaseModel


class ResponseError(BaseModel):
    code: int
    message: str


class EmptyObject(BaseModel):
    object: Union[None] = None


class ModbusServer(BaseModel):
    port: Union[str, None] = None
    rate: Union[int, None] = None
    read_mode: Union[str, None] = None
    slave_address: Union[int, None] = None
    fake_connect: Union[bool, None] = None


class TaskerInput(BaseModel):
    enabled: bool
    task_file_path: Union[str, None] = None


class TaskerOutput(TaskerInput):
    task_count: Union[int, None] = None
    tasks: Union[Dict[str, str], None] = None


class Task(BaseModel):
    enabled: bool
    task_name: str
    task_type: str
    task_args: str
    task_repeat: Union[int, None] = None
    # report
    report_type: Union[str, None] = None
    report_name: Union[str, None] = None
    report_path: Union[str, None] = None


class TaskUpdate(Task):
    enabled: Union[bool, None] = None
    task_type: Union[str, None] = None
    task_args: Union[str, None] = None
    task_repeat: Union[int, None] = None


class MapInfoRecord(BaseModel):
    device_name: str
    protocol: str
    slave_address: int
    rate: int


class MapDataRecord(BaseModel):
    address: str
    read_type: str
    description: Union[str, None] = None
    divide: Union[str, None] = None


class _MapperBody(BaseModel):
    info: MapInfoRecord
    data: Dict[str, MapDataRecord]


class DeviceMapper(BaseModel):
    device_mapper: _MapperBody
