import getopt
import sys

import IOperations as Io
from LoggerService import LoggerService
from PathProvider import PathProvider
from ExecutorService import ExecutorService


def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels>]')

    input_dir = PathProvider.input_250k
    zoom = '13'
    use_profile = False

    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = PathProvider.input_50k
        if opt == '-z':
            zoom = arg

    Io.makeDirectories(PathProvider.log_dir)

    logger_service = LoggerService()
    es = ExecutorService(input_dir, zoom, use_profile)
    es.execute('ray')
    logger_service.close()


if __name__ == '__main__':
    main(sys.argv[1:])
