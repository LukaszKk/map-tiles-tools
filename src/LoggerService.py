import time
import datetime
import psutil
import threading

from Logger import Logger


class LoggerService:

    def __init__(self, interval=600):
        self.logger = None
        self.init_time = 0
        self.interval = interval

        self.logger = Logger().create_logger()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.run)

        self.init_time = time.time()
        self.thread.start()

    def run(self):
        while True:
            self.log()
            time.sleep(self.interval)

    def log(self):
        time_passed = int(time.time() - self.init_time)
        time_delta = str(datetime.timedelta(seconds=time_passed))
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        self.logger.debug('Time running: ' + time_delta)
        self.logger.debug('CPU: {}%'.format(cpu_percent))
        self.logger.debug('RAM: {}%\n'.format(ram.percent))

    def log_message(self, message):
        self.logger.debug(message)

    def close(self):
        self.thread.join(10)
        self.log()

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
