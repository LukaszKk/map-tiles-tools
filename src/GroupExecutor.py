import ray

from CSVReader import CSVReader
from ProcessService import ProcessService
from PathProvider import PathProvider


class GroupExecutor:

    @staticmethod
    def singleExecute(groups_dir, group_nr, input_dir, zoom, use_profile):
        path_provider = PathProvider(str(group_nr) + "\\")
        groups_dir = PathProvider.groups_dir + str(groups_dir) + "\\"
        data = CSVReader.read_group(groups_dir, group_nr)
        ps = ProcessService(path_provider, data)

        if use_profile:
            ps.profileMerge(input_dir)
        else:
            ps.basicMerge(input_dir)
        ps.basicTile(zoom)

        return path_provider

    @staticmethod
    @ray.remote
    def rayExecute(groups_dir, group_nr, input_dir, zoom, use_profile):
        return GroupExecutor.singleExecute(groups_dir, group_nr, input_dir, zoom, use_profile)
