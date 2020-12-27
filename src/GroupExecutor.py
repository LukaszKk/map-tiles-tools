from CSVReader import CSVReader
from ProcessService import ProcessService
from PathProvider import PathProvider


class GroupExecutor:

    @staticmethod
    def singleExecute(group_nr, input_dir, zoom, use_profile):
        path_provider = PathProvider(str(group_nr) + "\\")
        data = CSVReader.read_group(group_nr)
        ps = ProcessService(path_provider, data)

        if use_profile:
            ps.profileMerge(input_dir)
        else:
            ps.basicMerge(input_dir)
        ps.basicTile(zoom)

        return path_provider
