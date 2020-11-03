import logging.handlers
import multiprocessing as mp

from PathProvider import PathProvider


class Logger:

    FILE = PathProvider.log_dir + 'logfile.log'
    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    @staticmethod
    def create_logger():
        logger = mp.get_logger()
        logger.setLevel(logging.DEBUG)

        handler = logging.handlers.RotatingFileHandler(filename=Logger.FILE, backupCount=8)
        handler.doRollover()
        handler.setFormatter(Logger.FORMATTER)
        logger.addHandler(handler)

        return logger
