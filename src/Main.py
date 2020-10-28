import getopt
import sys

import Transformations as Tr
import IOperations as Io
import Comparator as Cp
from LoggerService import LoggerService
from PathProvider import PathProvider


def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels>]')

    input_dir = PathProvider.input_250k
    zoom = '11'

    use_profile = False
    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = PathProvider.input_50k
        if opt == '-z':
            zoom = arg

    Io.makeDirectory(PathProvider.log_dir)
    logger_service = LoggerService()

    warp_in_file = PathProvider.merged_file
    if use_profile:
        Io.copyFiles(src=input_dir, dest=PathProvider.output_tmp_path)
        Tr.profileToProfile(input_data=PathProvider.output_tmp_path, out_path=PathProvider.output_tmp2_path)

        Io.copyFiles(src=PathProvider.output_tmp_path, dest=PathProvider.output_tmp2_path,
                     file_name_regex="*.TFW", delete_dest_before_copy=False)
        Tr.translateIntoOneFile(input_data=PathProvider.output_tmp2_path, out_path=PathProvider.output_data_path)

        Io.deleteDirectory(path=PathProvider.output_tmp_path)
        Io.deleteDirectory(path=PathProvider.output_tmp2_path)
        Tr.gdalMerge(input_data=PathProvider.output_data_path, out_file=PathProvider.merged_file)
    else:
        Io.copyFiles(src=input_dir, dest=PathProvider.output_data_path)
        Tr.gdalMerge(input_data=PathProvider.output_data_path, out_file=PathProvider.merged_file, is_pct=True)
        # Tr.gdalTranslate(input_file=PathProvider.merged_file, out_file=PathProvider.translated_file)
        # warp_in_file = PathProvider.translated_file
    # Tr.gdalWarp(in_file=warp_in_file, out_file=PathProvider.warped_file)
    # Tr.gdal2Tiles(in_file=PathProvider.warped_file, out_dir=PathProvider.output_tiles_path, zoom=zoom)

    logger_service.close()


def compare(argv=None):
    Cp.main(argv=argv)


if __name__ == '__main__':

    main(sys.argv[1:])
    # compare(sys.argv[1:])
