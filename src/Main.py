import getopt
import sys

import Transformations as Tr
import IOperations as Io
import Comparator as Cp
from LoggerService import LoggerService
from PathProvider import PathProvider


def basicMerge(input_dir):
    Io.deleteDirectory(PathProvider.output_data_path)
    Io.makeDirectory(PathProvider.output_data_path)
    Io.copyFiles(src=input_dir, dest=PathProvider.output_data_path)

    Io.deleteFile(PathProvider.merged_file)
    Io.makeDirectory(PathProvider.output_merged_path)
    Tr.gdalMerge(input_data=PathProvider.output_data_path,
                 out_file=PathProvider.merged_file, is_pct=True)

    Io.deleteFile(PathProvider.translated_file)
    Tr.gdalTranslate(input_file=PathProvider.merged_file,
                     out_file=PathProvider.translated_file)


def profileMerge(input_dir):
    Io.deleteDirectory(PathProvider.output_tmp_path)
    Io.makeDirectory(PathProvider.output_tmp_path)
    Io.copyFiles(src=input_dir, dest=PathProvider.output_tmp_path,
                 file_name_regex="*.tif")

    print('Profiling')
    Io.deleteDirectory(PathProvider.output_tmp2_path)
    Io.makeDirectory(PathProvider.output_tmp2_path)
    Tr.profileToProfile(input_data=PathProvider.output_tmp_path,
                        out_path=PathProvider.output_tmp2_path)

    Io.copyFiles(src=input_dir, dest=PathProvider.output_tmp2_path,
                 file_name_regex="*.TFW")

    print('Translating into one file...')
    Io.makeDirectory(PathProvider.output_data_path)
    Tr.translateIntoOneFile(input_data=PathProvider.output_tmp2_path,
                            out_path=PathProvider.output_data_path)

    Io.deleteDirectory(PathProvider.output_tmp_path)
    Io.deleteDirectory(PathProvider.output_tmp2_path)

    Io.deleteFile(PathProvider.merged_file)
    Io.makeDirectory(PathProvider.output_merged_path)
    Tr.gdalMerge(input_data=PathProvider.output_data_path,
                 out_file=PathProvider.merged_file)

    # Io.deleteDirectory(PathProvider.output_data_path + '1\\')
    # Io.deleteDirectory(PathProvider.output_data_path + '2\\')
    # Io.deleteDirectory(PathProvider.output_data_path + '3\\')
    # Io.deleteDirectory(PathProvider.output_data_path + '4\\')

    # Io.makeDirectory(PathProvider.output_data_path + '1\\')
    # Io.makeDirectory(PathProvider.output_data_path + '2\\')
    # Io.makeDirectory(PathProvider.output_data_path + '3\\')
    # Io.makeDirectory(PathProvider.output_data_path + '4\\')

    # reg = ('HP', 'HT', 'HU', 'HW', 'HX', 'HY', 'HZ', 'NA', 'NB', 'NC', 'ND',
    #        'NF', 'NG', 'NH', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO')
    # Io.moveFiles(PathProvider.output_data_path, PathProvider.output_data_path + '1\\', regex=reg)
    # reg = ('NR', 'NS', 'NT', 'NU', 'NW', 'NX', 'NY', 'NZ', 'OV', 'SC', 'SD', 'SE', 'TA')
    # Io.moveFiles(PathProvider.output_data_path, PathProvider.output_data_path + '2\\', regex=reg)
    # reg = ('SH', 'SJ', 'SK', 'TF', 'TG', 'SM', 'SN', 'SO', 'SP', 'TL', 'TM')
    # Io.moveFiles(PathProvider.output_data_path, PathProvider.output_data_path + '3\\', regex=reg)
    # reg = ('SR', 'SS', 'ST', 'SU', 'TQ', 'TR', 'SV', 'SW', 'SX', 'SY', 'SZ', 'TV')
    # Io.moveFiles(PathProvider.output_data_path, PathProvider.output_data_path + '4\\', regex=reg)

    # print('Merge 1')
    # Tr.gdalMerge(input_data=PathProvider.output_data_path + '1\\',
    #              out_file=PathProvider.output_merged_path + 'merged1.tif')
    # print('Merge 2')
    # Tr.gdalMerge(input_data=PathProvider.output_data_path + '2\\',
    #              out_file=PathProvider.output_merged_path + 'merged2.tif')
    # print('Merge 3')
    # Tr.gdalMerge(input_data=PathProvider.output_data_path + '3\\',
    #              out_file=PathProvider.output_merged_path + 'merged3.tif')
    # print('Merge 4')
    # Tr.gdalMerge(input_data=PathProvider.output_data_path + '4\\',
    #              out_file=PathProvider.output_merged_path + 'merged4.tif')
    # print('Merge all')
    # Tr.gdalMerge(input_data=PathProvider.output_merged_path,
    #              out_file=PathProvider.merged_file)


def basicTile(warp_in_file, zoom):
    print('Warping')
    Io.deleteFile(PathProvider.warped_file)
    Tr.gdalWarp(in_file=warp_in_file, out_file=PathProvider.warped_file)

    print('Tiling')
    Io.deleteDirectory(PathProvider.output_tiles_path)
    Io.makeDirectory(PathProvider.output_tiles_path)
    Tr.gdal2Tiles(in_file=PathProvider.warped_file,
                  out_dir=PathProvider.output_tiles_path,
                  zoom=zoom)


def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels>]')

    input_dir = PathProvider.input_250k
    zoom = '13'

    use_profile = False
    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = PathProvider.input_50k_incomplete
        if opt == '-z':
            zoom = arg

    Io.makeDirectory(PathProvider.log_dir)
    logger_service = LoggerService()

    if use_profile:
        profileMerge(input_dir)
        warp_in_file = PathProvider.merged_file
    else:
        basicMerge(input_dir)
        warp_in_file = PathProvider.translated_file
    basicTile(warp_in_file, zoom)

    logger_service.close()


def compare(argv=None):
    Cp.main(argv=argv)


if __name__ == '__main__':

    main(sys.argv[1:])
    # compare(sys.argv[1:])
