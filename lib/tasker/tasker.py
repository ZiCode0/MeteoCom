import json
import threading
import time
import schedule

from lib.modbus import server
from lib.tasker import task
from lib.mapping import mapper
from lib.workspace import workspace as ws
from lib.tasker.task_line import parse_read_line as ptl

workspace = ws.Workspace()  # workspace instance


class Task:
    def __init__(self, name, args, m_server, d_mapper):
        global workspace
        self.name = name
        self.args = args
        self.ms = m_server
        self.dm = d_mapper
        workspace.add_dataframe(name, ptl(self.args['task_line']).keys())
        # print()  # enable for #debug


class RTask(Task):
    def __init__(self, name, args, m_server, d_mapper):
        super().__init__(name, args, m_server, d_mapper)
        if args['report_type'] in ['text', 'excel']:
            self.export_path = task.make_export_path(self.args, self.dm)
        else:
            self.export_path = None

    def start_body(self):
        # get data
        task_data = task.get_set_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        # add row to dataframe
        workspace.add_row(self.name, task_data)
        # export last record
        workspace.export_last_row(name=self.name,
                                  export_path=self.export_path,
                                  method=self.args['report_type'])
        print(f'{self.name} {task_data}')


class WTask(Task):
    def start_body(self):
        # get data
        # task_data = task.get_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        task.get_set_data(args=self.args, modbus_server=self.ms, device_mapper=self.dm)
        print(f'{self.name} write function: done')


class Tasker:
    """
    Tasker instance to control input tasks: read, write, cmd input commands
    """
    def __init__(self, file_path, modbus_server, device_mapper):
        self.task_file_path = file_path
        self.modbus_server = modbus_server
        self.device_mapper = device_mapper
        self.exit_flag = False
        self.tasks_dict = self.read_config()  # Task parsable dictionary
        self.tasks = self.parse_tasks()  # init Task() list
        self.first_task_objs = []  # list for first tasks start
        self.starter_thread = threading.Thread(target=self.starter)  # Task() starter thread

    def read_config(self):
        file_obj = open(self.task_file_path, 'r').read()
        result = json.loads(file_obj)['tasks']
        # TODO: run schemas validator
        return result

    def parse_tasks(self):
        """
        Prepare tasks for working.
        Initialize Task() instances
        :return:
        """
        result_tasks = []
        for task_name in self.tasks_dict:
            if self.tasks_dict[task_name]['task_type'] == 'read':
                # add tasks instances to list
                tsk = RTask(name=task_name,
                            args=self.tasks_dict[task_name],
                            m_server=self.modbus_server,
                            d_mapper=self.device_mapper)
                result_tasks.append(tsk)
            if self.tasks_dict[task_name]['task_type'] == 'write':
                tsk = WTask(name=task_name,
                            args=self.tasks_dict[task_name],
                            m_server=self.modbus_server,
                            d_mapper=self.device_mapper)
                result_tasks.append(tsk)
        return result_tasks

    def starter(self):
        """
        Starter function to run tasks by scheduler. Should be started in thread.
        :return:
        """
        # tasks: first run
        for job in self.first_task_objs:
            job()
        # tasks: scheduled loop
        while True:
            # stop tasks by exit flag
            if self.exit_flag:
                break
            # run tasks
            schedule.run_pending()
            # reduce timer
            time.sleep(1)
        # stop all tasks if exit_flag
        schedule.clear()

    def start(self):
        """
        Start all tasks in time
        :return:
        """
        self.exit_flag = False
        # plan tasks running on time
        for o_task in self.tasks:
            schedule.every(o_task.args['task_repeat']).seconds.do(o_task.start_body)
            # add first once run
            self.first_task_objs.append(o_task.start_body)
        # start al tasks
        self.starter_thread.start()

    def stop(self):
        """
        Stop all running tasks
        :return:
        """
        self.exit_flag = True
