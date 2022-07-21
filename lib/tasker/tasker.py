import datetime
import json
import os

from lib.tasker import task, freq_task, ExTaskObjectNotFound, ExTaskObjectRemoveError

from lib.workspace.workspace import Workspace
from lib.modbus.mb_server import MServer
from lib.mapping.mapper import DeviceMapper
from lib.tasker.task_args import parse_read_line as ptl


class Task:
    def __init__(self, name: str, args: dict,
                 workspace: Workspace, m_server: MServer, d_mapper: DeviceMapper, logger=None):
        # global v_workspace
        self.name = name
        self.enabled = args['enabled']

        self.args = args
        self.ms = m_server
        self.dm = d_mapper
        self.logger = logger

        # self.nm = nm
        self.ws = workspace
        self.ws.add_dataframe(name, ptl(self.args['task_args']).keys())
        self.backup_mode = False

    def print_debug(self, string: str, level='info'):
        """
        Print debugging information function using native print() or logger object
        :param string: target string to output
        :param level: debugger object level
        """
        if self.logger:
            if level == 'info':
                self.logger.info(string)
            elif level == 'warning':
                self.logger.warning(string)
            elif level == 'error':
                self.logger.error(string)
        else:
            print(string)

    def get_object_dict(self):
        """
        Get object vars as dict
        :return:
        """
        return {
            "name": self.name,
            "enabled": self.enabled,
            "task_type": self.args["task_type"],
            "task_args": self.args,
            "task_repeat": self.args["task_repeat"]
        }


class RTask(Task):
    def __init__(self, name, args, workspace, m_server, d_mapper, logger=None):
        super().__init__(name, args, workspace, m_server, d_mapper, logger)
        if args['report_type'] in ['text', 'excel']:
            self.args['task_name'] = name
            # self.export_path = self.export_path()
        else:
            self.export_path = None
        # print()  # enable for #debug

    def export_path(self):
        return task.make_export_path(self.args, self.dm)

    def start_body(self):
        # get data
        task_data = task.get_set_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        # add row to dataframe
        self.ws.add_row(self.name, task_data)

        if self.backup_mode:
            export_file_name = self.ws.backup_connection.project_backup_file.format(
                datetime=datetime.datetime.now().strftime('%Y-%m-%d'),
                backup_name=self.name)
            self.ws.export_last_row(name=self.name,
                                    export_path=export_file_name,  # self.export_path,
                                    method='text')
            # TODO: enable ability to auto-reconnect
            # add last record to backup db
            # try to export data
            # if success to export data => self.backup_mode = False, erase backup db
        else:
            # export last record
            self.ws.export_last_row(name=self.name,
                                    export_path=self.export_path(),
                                    method=self.args['report_type'])
        # print debug info
        output_str = f'Task: {self.name} - {task_data}'
        self.print_debug(output_str)


class WTask(Task):
    def start_body(self):
        # get data
        # task_data = task.get_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        task.get_set_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        # print debug info
        output_str = f'{self.name} write function: done'
        self.print_debug(output_str)


class Tasker:
    """
    Tasker instance to control input tasks: read, write, cmd input commands
    """

    def __init__(self, modbus_server: MServer, device_mapper: DeviceMapper,
                 file_path=None, logger=None):
        self.task_file_path = file_path
        self.modbus_server = modbus_server
        self.device_mapper = device_mapper
        self.logger = logger

        self.ws = Workspace()

        # get 'enabled' tasker state True/False
        self.enabled = False

        self.exit_flag = False
        self.server_mode = False

        # self.tasks_dict = Union[Dict]
        self.task_objects = {}  # Union[Dict[Union[Task, RTask, WTask]]]
        self.task_jobs = {}  # Union[Dict[freq_task.FrequencyTask]]

        # if file path tasks
        if self.task_file_path or self.task_file_path == 'tasks.json':
            # configs parse dictionary
            _config_dict = self._read_config()
            # task dict to task objects
            self.task_objects = self._parse_dict_tasks(_config_dict)  # init Task() list
        # if empty tasks list for server mode
        else:
            self.task_objects = {}

    def _read_config(self):
        file_obj = open(self.task_file_path, 'r').read()
        config_dict = json.loads(file_obj)['tasks']
        # TODO: run schemas validator
        return config_dict

    def _parse_dict_tasks(self, config_dict):
        """
        Prepare tasks for work.
        Initialize Task() instances
        :return:
        """
        result_tasks = {}
        for task_name, task_dict in config_dict.items():
            if task_dict['task_type'] == 'read':
                # add tasks instances to list
                tsk = RTask(name=task_name,
                            args=config_dict[task_name],
                            workspace=self.ws,
                            m_server=self.modbus_server,
                            d_mapper=self.device_mapper,
                            logger=self.logger)
                result_tasks[task_name] = tsk
            elif task_dict['task_type'] == 'write':
                tsk = WTask(name=task_name,
                            args=config_dict[task_name],
                            workspace=self.ws,
                            m_server=self.modbus_server,
                            d_mapper=self.device_mapper)
                result_tasks[task_name] = tsk
            elif task_dict['task_type'] == 'server':
                self.server_mode = True

        return result_tasks

    def start(self):
        """
        Start all tasks in time
        :return:
        """
        self.exit_flag = False
        # plan tasks running on time
        for o_task_name, o_task_obj in self.task_objects.items():
            # make job instance
            task_job = freq_task.FrequencyTask(t_function=o_task_obj.start_body,
                                               t_sec_interval=o_task_obj.args['task_repeat'])

            # add to job list and start task if 'enabled' in task schema
            if self.task_objects[o_task_name].enabled:
                # add task job to buffer
                self.task_jobs[o_task_name] = task_job
                # start task
                self.task_jobs[o_task_name].start()

        # set 'tasker' active status
        self.enabled = True

    def stop(self):
        """
        Stop all running tasks
        :return:
        """
        for task_name, task_job in self.task_jobs.items():
            task_job.stop()
            # mark task as enabled
            self.task_objects[task_name].enabled = False
        # set disabled status
        self.enabled = False

    def _create_task_class_object(self, task_type: str, name: str, args: dict):  # -> Union[RTask, WTask, False]:
        """
        Create task object
        :return: Task object / False
        """
        response = False
        try:
            if task_type == 'read':
                response = RTask(name=name, args=args,
                                 workspace=self.ws,
                                 m_server=self.modbus_server, d_mapper=self.device_mapper, logger=self.logger)
            elif task_type == 'write':
                response = WTask(name=name, args=args,
                                 workspace=self.ws,
                                 m_server=self.modbus_server, d_mapper=self.device_mapper, logger=self.logger)
        finally:
            return response

    @staticmethod
    def _gen_server_task_object():
        """
        Return server task dict object to export
        :return:
        """
        return {'server': {'task_type': 'server'}}

    def task_add(self, enabled: bool, t_type: str, name: str, args: dict, task_repeat: int) -> bool:
        """
        Add task on hot-plug
        :param enabled: enable flag
        :param t_type: set task type. Ex: 'read' or 'write'
        :param name: set name for task
        :param args: input task dictionary
        :param task_repeat: repeat task each input seconds
        :return: add Task object result
        """
        response = False
        try:
            # create object instance
            task_object = self._create_task_class_object(task_type=t_type, name=name, args=args)
            if task_object:
                # make job instance
                task_job = freq_task.FrequencyTask(t_function=task_object.start_body,
                                                   t_sec_interval=task_repeat)
                self.task_objects[task_object.name] = task_object
                self.task_jobs[task_object.name] = task_job
                if enabled:
                    self.task_jobs[task_object.name].start()
                    self.task_objects[task_object.name].enabled = True

                response = True
        finally:
            return response

    def task_remove(self, task_name: str) -> bool:
        """
        Remove task on hot-plug
        :param task_name: target task name
        :return: :type bool: add Task object result
        """
        if task_name in self.task_objects:
            try:
                # stop job if enabled
                if self.task_objects[task_name].enabled:
                    # stop job
                    self.task_jobs[task_name].stop()
                # remove task from tasker buffers
                del self.task_jobs[task_name]
                del self.task_objects[task_name]
                return True
            except Exception:
                raise ExTaskObjectRemoveError(task_name=task_name)
        else:
            raise ExTaskObjectNotFound(task_name=task_name)

    def task_start(self, task_name: str) -> bool:
        self.task_jobs[task_name].start()
        return True

    def task_stop(self, task_name: str) -> bool:
        self.task_jobs[task_name].stop()
        return True

    def get_status(self) -> bool:
        return self.enabled

    def get_tasks_count(self):
        return len(self.task_objects)

    def get_tasks_dict(self):
        # get task vars from .args param
        resp_dict = {key: value.args for (key, value) in self.task_objects.items()}
        # return with run status param
        for key, val in resp_dict.items():
            resp_dict[key]['enabled'] = self.task_objects[key].enabled
        return resp_dict

    def get_tasks_dict_as_list(self):
        # return dict as list
        return [val for val in self.get_tasks_dict().values()]

    def get_tasks_status_dict(self):
        def get_enabled_str(status: bool):
            return 'enabled' if status else 'disabled'
        return {key: get_enabled_str(value.enabled) for (key, value) in self.task_objects.items()}  # list(self.task_objects.keys())

    def get_task_file_path(self):
        return self.task_file_path

    def export_json(self, file_path='./tasks.json', get_object=False) -> str:
        """
        Export tasks file in json format
        :param file_path :type str: target file path to export
        :param get_object :type bool flag to return file object
        """

        # replace "dot" with absolute path > link with "cwd" folder
        if file_path.startswith('./'):
            cwd = os.getcwd()
            file_path = file_path.replace('.', cwd, 1)
        # if in-project folder file input > put in "cwd" folder
        if '/' not in file_path:
            cwd = os.getcwd()
            file_path = f'{cwd}/{file_path}'

        # dump device map
        export_dict = self.get_tasks_dict()
        # add server task if enabled
        if self.server_mode:
            export_dict.update(self._gen_server_task_object())
        # add header
        export_dict = {'tasks': export_dict}

        # export json
        json_tasks = json.dumps(export_dict, indent=4)
        # call return
        if get_object:
            return json_tasks
        else:
            # export to file
            with open(file_path, 'w') as f:
                f.write(json_tasks)
            return file_path
