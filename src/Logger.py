import logging.handlers
import multiprocessing as mp


class Logger:

    FILE = 'logfile.log'
    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    @staticmethod
    def create_logger(path_provider):
        logger = mp.get_logger()
        logger.setLevel(logging.DEBUG)
        filename = path_provider.log_dir + Logger.FILE

        handler = logging.handlers.RotatingFileHandler(filename=filename, backupCount=8)
        handler.doRollover()
        handler.setFormatter(Logger.FORMATTER)
        logger.addHandler(handler)

        return logger
