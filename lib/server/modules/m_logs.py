from fastapi import HTTPException, APIRouter
from starlette.responses import StreamingResponse

router = APIRouter(
    tags=["Logs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/logs_app")
async def get_app_logs():
    """Get application logs"""
    try:
        log_file_name = "MeteoCom.log"
        with open(log_file_name, "r") as f:
            response = StreamingResponse(iter([f.read()]), media_type="text/csv")
            response.headers["Content-Disposition"] = f"attachment; filename={log_file_name}"
            return response
    # return error
    except Exception as ex:
        raise HTTPException(status_code=500, detail=repr(ex))
