import os

import logging


class Logger:

    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = src_dir + '\\..\\log\\'
    FILE = log_dir + 'logfile.log'
    FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.FILE)
        handler.setFormatter(self.FORMATTER)
        self.logger.addHandler(handler)

    def log(self):
        self.logger.info('Information')
