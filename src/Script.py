import os
import subprocess
import time
import rasterio.merge
from pathlib import Path
import IOperations as Io
from PIL import Image
from PIL import ImageCms

Image.MAX_IMAGE_PIXELS = None

env_path = 'C:\\Users\\obliczenia\\anaconda3\\envs\\geo3\\'
scripts_path = env_path + 'Scripts\\'
src_dir = os.path.dirname(os.path.abspath(__file__))

input_dir = src_dir + '\\..\\input\\data\\50kTmp\\'
output_data_path = src_dir + '\\..\\output\\data\\'
output_data2_path = src_dir + '\\..\\output\\tmp\\'
output_data3_path = src_dir + '\\..\\output\\tmp2\\'
output_merged_path = src_dir + '\\..\\output\\merged\\'
merged_file = output_merged_path + 'merged.tif'
translated_file = output_merged_path + 'translated.tif'
warped_file = output_merged_path + 'warped.tif'
output_tiles_path = src_dir + '\\..\\output\\tiles\\'
input_path = src_dir + '\\..\\input\\'
input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'
zoom = '11'

# ==============================================================================

for j in range(1, 2):
    input_dir_x = input_dir + '{}\\'.format(j)
    output_data_path_x = output_data_path + '{}\\'.format(j)
    output_data2_path_x = output_data2_path + '{}\\'.format(j)
    output_data3_path_x = output_data3_path + '{}\\'.format(j)
    output_merged_path_x = output_merged_path + '{}\\'.format(j)
    output_tiles_path_x = output_tiles_path + '{}\\'.format(j)
    merged_file = output_merged_path_x + 'merged.tif'
    translated_file = output_merged_path_x + 'translated.tif'
    warped_file = output_merged_path_x + 'warped.tif'

    # print('Copying input data')
    # Io.deleteDirectory(output_data_path_x)
    # Io.makeDirectories(output_data_path_x)
    # Io.copyFiles(src=input_dir_x, dest=output_data_path_x, file_name_regex="*.tif")
    #
    # #
    #
    # Io.deleteDirectory(output_data2_path_x)
    # Io.makeDirectories(output_data2_path_x)
    #
    # files = Io.getFilesList(output_data_path_x)
    # for image in files:
    #     in_image = Image.open(image)
    #
    #     out_im = ImageCms.profileToProfile(im=in_image,
    #                                        inputProfile=input_icc,
    #                                        outputProfile=output_icc,
    #                                        outputMode='RGB')
    #     file_name = image.split('\\')
    #     file_name_len = len(file_name)
    #     file_name = file_name[file_name_len - 1]
    #     out_im.save(output_data2_path_x + file_name)
    #
    # Io.copyFiles(src=input_dir_x, dest=output_data2_path_x, file_name_regex="*.TFW")
    #
    # # Io.deleteDirectory(output_data3_path_x)
    # # Io.makeDirectories(output_data3_path_x)
    # #
    # # files = Io.getFilesList(output_data2_path_x)
    # # for file in files:
    # #     file_name = file.split('\\')
    # #     file_name_len = len(file_name)
    # #     file_name = file_name[file_name_len - 1]
    # #     params = [
    # #         '-b', '1',
    # #         '-b', '2',
    # #         '-b', '3',
    # #         '-a_srs', 'EPSG:27700',
    # #         '-of', 'GTiff',
    # #         '-co', 'PHOTOMETRIC=RGB',
    # #         '-co', 'COMPRESS=DEFLATE',
    # #         '-co', 'BIGTIFF=YES',
    # #         file,
    # #         output_data3_path_x + file_name
    # #     ]
    # #     subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)
    #
    # output_data_path_x = output_data2_path_x
    #
    # #
    #
    # print('Merging...')
    # Io.deleteFile(merged_file)
    # Io.makeDirectories(output_merged_path_x)
    #
    # files_to_merge = Io.getFilesList(output_data_path_x)
    #
    is_pct = False
    # if is_pct:
    #     additional_options = ['-a_nodata', '255',
    #                           '-pct']
    # else:
    #     additional_options = ['-a_nodata', '0',
    #                           '-co', 'PHOTOMETRIC=RGB']
    # params = additional_options + [
    #     '-of', 'GTiff',
    #     '-co', 'COMPRESS=DEFLATE',
    #     '-co', 'BIGTIFF=YES',
    #     '-o', merged_file
    # ]
    # params = params + files_to_merge
    # subprocess.call(["python", scripts_path + "gdal_merge.py"] + params)

    print('Translating...')
    Io.deleteFile(translated_file)

    if is_pct:
        additional_options = ['-expand', 'rgb']
    else:
        additional_options = ['-b', '1',
                              '-b', '2',
                              '-b', '3']

    params = additional_options + [
        '-ot', 'Byte',
        '-of', 'GTiff',
        '-a_srs', 'EPSG:27700',
        '-a_nodata', '0',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=YES',
        merged_file,
        translated_file
    ]
    subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)

    warp_in_file = translated_file

    print('Warping')
    Io.deleteFile(warped_file)

    params = [
        '-ot', 'Byte',
        '-of', 'GTiff',
        '-s_srs', 'EPSG:27700',
        '-t_srs', 'EPSG:3857',
        '-srcnodata', '0',
        '-dstnodata', '0',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=YES',
        warp_in_file,
        warped_file
    ]
    subprocess.call([env_path + 'Library\\bin\\gdalwarp.exe'] + params)

    print('Tiling')
    Io.deleteDirectory(output_tiles_path_x)
    Io.makeDirectories(output_tiles_path_x)
    path = Path(output_tiles_path_x)

    params = [
        '-s', 'EPSG:3857',
        '-z', zoom,
        '-w', 'openlayers',
        '--xyz',
        '-a', '0',
        '-x',
        warped_file,
        output_tiles_path_x
    ]
    subprocess.call(["python", scripts_path + 'gdal2tiles.py'] + params)

    count = sum(1 for x in path.glob('**/*') if x.is_file())
    print('FILES COUNT: {}'.format(count))
