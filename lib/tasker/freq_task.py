import multiprocessing
import threading
import time


class FrequencyTask:
    def __init__(self, t_function, t_sec_interval=1, stopper=None, *args, **kwargs):
        # thread settings
        self.daemon = False
        self.stopper = stopper if stopper else threading.Event()
        # task body args
        self.target_interval = t_sec_interval
        self.target_func = t_function
        self.args = args
        self.kwargs = kwargs
        # thread function task
        self.proc = multiprocessing.Process(target=self.body_function, daemon=self.daemon)

    def body_function(self):
        try:
            while not self.stopper.is_set():
                # set precision param
                precision_param = 5
                # get timer value
                timer_value = time.time() % self.target_interval
                # check timer
                if round(timer_value, precision_param) == self.target_interval:
                    # run target
                    self.target_func(**self.kwargs)
        except KeyboardInterrupt:
            self.stopper.set()

    def stop(self):
        self.stopper.set()
        self.proc.kill()
        self.proc.join()

    def start(self):
        self.proc.start()


def _test_func_1(**kwargs):
    import datetime
    print(f'{datetime.datetime.now()} : test_1\n')


def _test_func_2(**kwargs):
    import datetime
    print(f'{datetime.datetime.now()} : test_2 : kwargs - {kwargs}\n')


if __name__ == "__main__":
    _test_job1 = FrequencyTask(t_function=_test_func_1, t_sec_interval=1, aa=1, bb=2)
    _test_job2 = FrequencyTask(t_function=_test_func_2, t_sec_interval=2, aa=1, bb=2)
    _test_job1.start()
    _test_job2.start()
    time.sleep(11)
    _test_job1.stopper.set()
    _test_job2.stopper.set()
