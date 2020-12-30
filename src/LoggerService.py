import time
import datetime
import psutil
import threading

from Logger import Logger


class LoggerService:

    def __init__(self, interval=600, backup_count=8):
        self.logger = None
        self.init_time = 0
        self.interval = interval

        self.logger = Logger().create_logger(backup_count)
        self.thread = threading.Thread(target=self.run)
        self.lock = threading.Lock()
        self.stop = False

        self.log_available_resources()
        self.init_time = time.time()
        self.thread.start()

    def run(self):
        while not self.stop:
            self.log()
            time.sleep(self.interval)

    def log(self):
        with self.lock:
            time_passed = int(time.time() - self.init_time)
            time_delta = str(datetime.timedelta(seconds=time_passed))
            cpu_percent = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            self.logger.debug('Time running: ' + time_delta)
            self.logger.debug('CPU: {}%'.format(cpu_percent))
            self.logger.debug('RAM: {}%\n'.format(ram.percent))

    def log_available_resources(self):
        with self.lock:
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            ram = psutil.virtual_memory().total
            self.logger.debug('CPU count: {}'.format(cpu_count))
            self.logger.debug('CPU frequency: {}'.format(cpu_freq))
            self.logger.debug('Total RAM: {}\n'.format(ram))

    def log_message(self, message):
        with self.lock:
            self.logger.info(message)

    def close(self):
        self.stop = True
        self.log()
