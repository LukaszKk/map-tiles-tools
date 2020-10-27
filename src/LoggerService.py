import time
import datetime
import multiprocessing as mp
import psutil

from Logger import Logger


class LoggerService:

    init_time = 0
    delay = 5

    def __init__(self):
        self.logger = None
        self.logger_instance = Logger()
        self.pool = mp.Pool(mp.cpu_count())
        self.pool.apply_async(self.run)

    def run(self):
        self.logger = self.logger_instance.create_logger()
        self.init_time = time.time()
        while True:
            self.log()
            time.sleep(self.delay)

    def log(self):
        time_passed = int(time.time() - self.init_time)
        time_delta = str(datetime.timedelta(seconds=time_passed))
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        self.logger.debug('Time running: ' + time_delta)
        self.logger.debug('CPU: {}'.format(cpu_percent))
        self.logger.debug('RAM used: {}'.format(ram_percent))

    def close(self):
        self.log()
        self.pool.close()
        self.pool.join()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
