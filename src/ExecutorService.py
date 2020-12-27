import multiprocessing as mp
import IOperations as Io

from CSVReader import CSVReader
from ProcessService import ProcessService
from NoDaemonProcessPool import NoDaemonProcessPool
from PathProvider import PathProvider


class ExecutorService:

    def __init__(self, input_dir, zoom, use_profile):
        self.input_dir = input_dir
        self.zoom = zoom
        self.use_profile = use_profile

    def __singleExecute(self, group_nr):
        path_provider = PathProvider(str(group_nr) + "\\")
        data = CSVReader.read_group(group_nr)
        ps = ProcessService(path_provider, data)

        if self.use_profile:
            ps.profileMerge(self.input_dir)
        else:
            ps.basicMerge(self.input_dir)
        ps.basicTile(self.zoom)

        return path_provider.output_tiles_path

    def __singleRun(self):
        path_provider = PathProvider()
        ps = ProcessService(path_provider)

        if self.use_profile:
            ps.profileMergeSingleRun(self.input_dir)
        else:
            ps.basicMerge(self.input_dir)
        ps.basicTile(self.zoom)

    def __groupRun(self):
        count = Io.getFilesCount(PathProvider.groups_dir)
        params = [(i, ) for i in range(1, count)]
        with NoDaemonProcessPool(mp.cpu_count()) as p:
            src_paths = p.starmap(self.__singleExecute, params)
            p.close()
            p.join()

        Io.mergeTiles(src_paths, PathProvider().output_tiles_path, self.zoom)

    def execute(self, method):
        if method == 'single':
            self.__singleRun()
        elif method == 'group':
            self.__groupRun()
