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
    method = 'single'
    groups = '3'

    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = PathProvider.input_50k
        if opt == '-z':
            zoom = arg
        if opt == '-m':
            method = arg
        if opt == '-g':
            groups = arg
    if not use_profile:
        groups = groups + '-250'

    # --- Temp TODO: delete
    if not use_profile:
        zoom = '11'
        input_dir = PathProvider.input_250k
    else:
        zoom = '13'
        input_dir = PathProvider.input_50k
    # ---

    Io.makeDirectories(PathProvider.log_dir)

    logger_service = LoggerService(groups, method, interval=10, backup_count=15)

    logger_service.start()
    es = ExecutorService(groups, input_dir, zoom, use_profile)
    es.execute(method)
    logger_service.close()
    print("EXIT")


if __name__ == '__main__':
    main(sys.argv[1:])
