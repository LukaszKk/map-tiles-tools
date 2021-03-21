import multiprocessing as mp
import IOperations as Io
import ray
import concurrent.futures

from ProcessService import ProcessService
from NoDaemonProcessPool import NoDaemonProcessPool
from PathProvider import PathProvider
from GroupExecutor import GroupExecutor


class ExecutorService:

    def __init__(self, groups, input_dir, zoom, use_profile):
        self.groups_dir = PathProvider.groups_dir + str(groups) + "\\"
        self.input_dir = input_dir
        self.zoom = zoom
        self.use_profile = use_profile

    def __singleRun(self):
        path_provider = PathProvider()
        ps = ProcessService(path_provider)

        if self.use_profile:
            ps.profileMergeSingleRun(self.input_dir, self.use_profile, self.zoom)
        else:
            ps.basicMerge(self.input_dir)
            ps.basicTile(not self.use_profile, self.zoom)
            Io.deleteDirectory(path_provider.output_data_path)
            Io.deleteDirectory(path_provider.output_merged_path)

    def mergeTiles(self, path_providers):
        print("Merging tiles...")
        src_paths = [provider.output_tiles_path for provider in path_providers]
        Io.mergeTiles(src_paths, PathProvider().output_tiles_path, self.zoom)

        for provider in path_providers:
            Io.deleteDirectory(provider.output_path)

    def __groupRunMultithreading(self):
        count = Io.getFilesCount(self.groups_dir)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                GroupExecutor.singleExecute, self.groups_dir, i, self.input_dir,
                self.zoom, self.use_profile)
                for i in range(1, count + 1)]
            path_providers = [future.result() for future in futures]
        self.mergeTiles(path_providers)

    def __groupRunMultiprocessing(self):
        count = Io.getFilesCount(self.groups_dir)
        params = [(self.groups_dir, i, self.input_dir, self.zoom, self.use_profile)
                  for i in range(1, count + 1)]
        with NoDaemonProcessPool(mp.cpu_count()) as p:
            path_providers = p.starmap(GroupExecutor.singleExecute, params)
            p.close()
            p.join()
        self.mergeTiles(path_providers)

    def __groupRunRay(self):
        ray.init(num_cpus=mp.cpu_count())
        count = Io.getFilesCount(self.groups_dir)
        path_providers = ray.get([GroupExecutor.rayExecute.remote(
            self.groups_dir, i, self.input_dir, self.zoom, self.use_profile)
            for i in range(1, count + 1)])
        self.mergeTiles(path_providers)

    def execute(self, method):
        if method == 'single' or method == 's':
            self.__singleRun()
        elif method == 'multithreading' or method == 'mt':
            self.__groupRunMultithreading()
        elif method == 'multiprocessing' or method == 'mp':
            self.__groupRunMultiprocessing()
        elif method == 'ray' or method == 'r':
            self.__groupRunRay()
