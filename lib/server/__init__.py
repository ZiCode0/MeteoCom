from fastapi import FastAPI

from starlette.staticfiles import StaticFiles

from lib.server import modules


app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(modules.router)

app.include_router(modules.m_modbus.router)
app.include_router(modules.m_tasker.router)
app.include_router(modules.m_mapper.router)

app.include_router(modules.m_task.router)
app.include_router(modules.m_data.router)
app.include_router(modules.m_logs.router)

app.include_router(modules.m_export.router)
