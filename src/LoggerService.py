import threading
import time

from Logger import Logger


class LoggerService:

    delay = 5

    def __init__(self):
        self.thread = LoggerThread(1, 'Thread-1', self.delay)
        self.thread.start()

    def join(self):
        self.thread.join()


class LoggerThread(threading.Thread):

    def __init__(self, thread_id, name, delay):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.delay = delay
        self.logger = Logger()

    def run(self):
        while True:
            self.logger.log()
            time.sleep(self.delay)
