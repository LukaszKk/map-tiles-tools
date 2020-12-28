import time
import datetime
import psutil
import multiprocessing as mp

from Logger import Logger


class LoggerService:

    def __init__(self, delay=600):
        self.logger = None
        self.init_time = 0
        self.delay = delay

        self.pool = mp.Pool(mp.cpu_count())
        self.pool.apply_async(self.run)

    def run(self):
        self.logger = Logger().create_logger()
        self.init_time = time.time()
        while True:
            self.log()
            time.sleep(self.delay)

    def log(self):
        if self.logger is None:
            return
        time_passed = int(time.time() - self.init_time)
        time_delta = str(datetime.timedelta(seconds=time_passed))
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        self.logger.debug('Time running: ' + time_delta)
        self.logger.debug('CPU: {}%'.format(cpu_percent))
        self.logger.debug('RAM: {}\n'.format(ram))

    def log_message(self, message):
        if self.logger is None:
            return
        self.logger.info(message)

    def close(self):
        self.pool.close()
        self.pool.terminate()
        self.log()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
