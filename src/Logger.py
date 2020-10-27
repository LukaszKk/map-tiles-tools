import os
import logging
import multiprocessing as mp


class Logger:

    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = src_dir + '\\..\\logs\\'
    FILE = log_dir + 'logfile.log'
    FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def create_logger(self):
        logger = mp.get_logger()
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.FILE, mode='w')
        handler.setFormatter(self.FORMATTER)
        logger.addHandler(handler)

        return logger
