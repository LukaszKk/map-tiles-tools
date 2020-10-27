import time
import datetime
import multiprocessing as mp

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
        self.logger.info('Time passed: ' + str(datetime.timedelta(seconds=time_passed)))

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
