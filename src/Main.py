import getopt
import sys

import IOperations as Io
import multiprocessing as mp
from NoDaemonProcessPool import NoDaemonProcessPool
from ExecutorService import ExecutorService
from LoggerService import LoggerService
from PathProvider import PathProvider
from CSVReader import CSVReader


def single_execute(group, input_dir, zoom, use_profile):
    path_provider = PathProvider(str(group) + "\\")
    data = CSVReader.read_group(group)
    es = ExecutorService(path_provider, data)

    Io.makeDirectories(path_provider.log_dir)
    logger_service = LoggerService(path_provider)

    if use_profile:
        es.profileMerge(input_dir)
    else:
        es.basicMerge(input_dir)
    es.basicTile(zoom)

    logger_service.close()


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

    with NoDaemonProcessPool(mp.cpu_count()) as p:
        p.starmap(single_execute, [(1, input_dir, zoom, use_profile),
                                   (2, input_dir, zoom, use_profile),
                                   (3, input_dir, zoom, use_profile), ])
        p.close()
        p.join()


if __name__ == '__main__':
    main(sys.argv[1:])
