import multiprocessing as mp
import IOperations as Io

from ProcessService import ProcessService
from NoDaemonProcessPool import NoDaemonProcessPool
from PathProvider import PathProvider
from GroupExecutor import GroupExecutor


class ExecutorService:

    def __init__(self, input_dir, zoom, use_profile):
        self.input_dir = input_dir
        self.zoom = zoom
        self.use_profile = use_profile

    def __singleRun(self):
        path_provider = PathProvider()
        ps = ProcessService(path_provider)

        if self.use_profile:
            ps.profileMergeSingleRun(self.input_dir)
        else:
            ps.basicMerge(self.input_dir)
        ps.basicTile(self.zoom)

        Io.deleteDirectory(path_provider.output_data_path)
        Io.deleteDirectory(path_provider.output_merged_path)

    def __groupRun(self):
        count = Io.getFilesCount(PathProvider.groups_dir)
        params = [(i, self.input_dir, self.zoom, self.use_profile) for i in range(1, count + 1)]
        with NoDaemonProcessPool(mp.cpu_count()) as p:
            path_providers = p.starmap(GroupExecutor.singleExecute, params)
            p.close()
            p.join()

        src_paths = [provider.output_tiles_path for provider in path_providers]
        Io.mergeTiles(src_paths, PathProvider().output_tiles_path, self.zoom)

        for provider in path_providers:
            Io.deleteDirectory(provider.output_path)

    def execute(self, method):
        if method == 'single':
            self.__singleRun()
        elif method == 'group':
            self.__groupRun()
