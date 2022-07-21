from fastapi import APIRouter
from starlette.responses import RedirectResponse

from . import m_data, m_logs, m_modbus, m_task, m_tasker, m_export, m_mapper


router = APIRouter()


@router.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs/')
