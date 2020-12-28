import logging.handlers

from PathProvider import PathProvider


class Logger:

    FILE = PathProvider.log_dir + 'logfile.log'
    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    def __init__(self):
        self.logger = None

    def create_logger(self):
        if self.logger is not None:
            return self.logger
        self.logger = logging.getLogger(Logger.__name__)

        handler = logging.handlers.RotatingFileHandler(filename=Logger.FILE,
                                                       backupCount=8)
        handler.doRollover()
        handler.setFormatter(Logger.FORMATTER)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

        return self.logger
