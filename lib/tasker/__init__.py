class ExTaskObjectNotFound(Exception):
    def __init__(self, task_name):
        super(ExTaskObjectNotFound, self).__init__()
        self.code = 404
        self.message = f'Task "{task_name}" was not found..'


class ExTaskObjectRemoveError(Exception):
    def __init__(self, task_name):
        super(ExTaskObjectRemoveError, self).__init__()
        self.code = 500
        self.message = f'Error removing "{task_name}"..'


class ExTaskerNotEnabled(Exception):
    def __init__(self):
        super(ExTaskerNotEnabled, self).__init__()
        self.code = 500
        self.message = 'Tasker not enabled'


class ExTaskerNotExist(Exception):
    def __init__(self):
        super(ExTaskerNotExist, self).__init__()
        self.code = 500
        self.message = 'Tasker instance not initialized'
