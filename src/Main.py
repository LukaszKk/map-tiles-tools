import getopt
import sys

import IOperations as Io
from LoggerService import LoggerService
from PathProvider import PathProvider
from ExecutorService import ExecutorService

'''
An application that generates raster data in XYZ format.

Requirements
    Gdal 3.1+ (conda install -c conda-forge/label/main gdal)
    
Parameters
    k : generate output of input data 50k. If not defined generates output of input data 250k
    z <level> : generate output data for defined <level>
    m <method> : use one of below methods as a simultaneous way of generation
        s, single : generate data without parallel mode. Parameter -g is ignored.
        mt, multithreading : use multiple threads in parallel mode 
        mp, multiprocessing : use multiple processes in parallel mode 
        r, ray : use ray library in parallel mode
    g <groups> : define number of groups to generate simultaneously
    
Example of execution
    50k
        python src\\Main.py -k -z 13 -m single -g 1
    250K
        python src\\Main.py -z 11 -m mp -g 7
'''
def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels> -m <method> -g <groups>]')

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
    # if not use_profile:
    #     zoom = '11'
    #     input_dir = PathProvider.input_250k
    # else:
    #     zoom = '13'
    #     input_dir = PathProvider.input_50k
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
