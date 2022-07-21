import uvicorn
from uvicorn_loguru_integration import run_uvicorn_loguru

from lib import server


class ErrorCreateObject(Exception):
    def __init__(self, i_object_type, i_object):
        self.code = 500
        self.message = f"Error creating '{i_object_type}': {repr(i_object)}"
        super().__init__(self.message)


class CWebServer:
    """Fast API Web server based on uvicorn. Starts as Process()"""

    def __init__(self, host='127.0.0.1', port=5000, log_level='info'):
        self.proc = None  # Process/Thread object var
        self.host = host
        self.port = port
        self.log_level = log_level

    def start(self):
        if not self.proc:
            self.run_server_func()
        else:
            self.stop()
            self.run_server_func()

    def stop(self):
        try:
            self.proc.kill()
        except:  # TODO: determine
            pass

    def run_server_func(self):
        # # default uvicorn run
        # uvicorn.run(app, host=self.host, port=self.port)
        # # run uvicorn with loguru support
        run_uvicorn_loguru(
            uvicorn.Config(
                app=server.app,
                host=self.host,
                port=self.port,
                log_level=self.log_level,
                reload=True,
            )
        )
