import getopt
import os
import sys

src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_dir)

import Transformations as Tr
import IOperations as Io
import Comparator as Cp

input_path = src_dir + '\\..\\input\\'
output_path = src_dir + '\\..\\output\\'

input_data_path = input_path + 'data\\'
output_data_path = output_path + 'data\\'
output_tmp_path = output_path + 'tmp\\'
output_tmp2_path = output_path + 'tmp2\\'
output_tiles_path = output_path + 'tiles\\'

input_50k = input_data_path + '50k\\'
input_50k_incomplete = input_data_path + '50kIncomplete\\'
input_50kTmp = input_data_path + '50kTmp\\'
input_250k = input_data_path + '250k\\'

output_merged_path = output_path + 'merged\\'
merged_file = output_merged_path + 'merged.tif'
warped_file = output_merged_path + 'warped.tif'
translated_file = output_merged_path + 'translated.tif'


def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels>]')
    input_dir = input_250k
    zoom = '11'

    use_profile = False
    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = input_50kTmp
        if opt == '-z':
            zoom = arg

    warp_in_file = merged_file
    if use_profile:
        Io.copyFiles(src=input_dir, dest=output_tmp_path)
        Tr.profileToProfile(input_data=output_tmp_path, out_path=output_tmp2_path)
        Io.copyFiles(src=output_tmp_path, dest=output_tmp2_path, file_name_regex="*.TFW", delete_dest_before_copy=False)
        Tr.translateIntoOneFile(input_data=output_tmp2_path, out_path=output_data_path)
        Io.deleteDirectory(path=output_tmp_path)
        Io.deleteDirectory(path=output_tmp2_path)
        Tr.gdalMerge(input_data=output_data_path, out_file=merged_file)
    else:
        Io.copyFiles(src=input_dir, dest=output_data_path)
        Tr.gdalMerge(input_data=output_data_path, out_file=merged_file, is_pct=True)
        Tr.gdalTranslate(input_file=merged_file, out_file=translated_file)
        warp_in_file = translated_file
    Tr.gdalWarp(in_file=warp_in_file, out_file=warped_file)
    Tr.gdal2Tiles(in_file=warped_file, out_dir=output_tiles_path, zoom=zoom)


def compare(argv=None):
    Cp.main(out_dir=output_tiles_path, argv=argv)


if __name__ == '__main__':

    main(sys.argv[1:])
    # compare(sys.argv[1:])
