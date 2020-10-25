import os
import subprocess
import sys

from PIL import Image
from PIL import ImageCms

src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_dir)

import IOperations as Io


Image.MAX_IMAGE_PIXELS = None

src_dir = os.path.dirname(os.path.abspath(__file__))
env_path = 'C:\\Users\\obliczenia\\anaconda3\\envs\\geo2\\'

input_path = src_dir + '\\..\\input\\'
output_path = src_dir + '\\..\\output\\'
scripts_path = env_path + 'Scripts\\'

output_merged_path = output_path + 'merged\\'


input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'


def profileToProfile(input_data, out_path):
    print("Profiling...")
    Io.makeDirectory(out_path)
    files = Io.getFilesList(input_data)
    for image in files:
        in_image = Image.open(image)

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc,
                                           outputMode='RGBA')
        file_name = image.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        out_im.save(out_path + file_name)


def translateIntoOneFile(input_data, out_path):
    Io.deleteDirectory(out_path)
    Io.makeDirectory(out_path)
    files = Io.getFilesList(input_data)
    for file in files:
        file_name = file.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        params = [
            '-b', '1',
            '-b', '2',
            '-b', '3',
            '-co', 'PHOTOMETRIC=RGB',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'BIGTIFF=IF_NEEDED',
            file,
            out_path + file_name
        ]
        subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalMerge(input_data, out_file, is_pct=False):
    print("Merging...")
    Io.deleteDirectory(output_merged_path)
    Io.makeDirectory(output_merged_path)
    files_to_merge = Io.getFilesList(input_data)
    if is_pct:
        additional_options = ['-pct']
    else:
        additional_options = ['-co', 'PHOTOMETRIC=RGB']
    params = additional_options + [
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=IF_NEEDED',
        '-o', out_file]
    params = params + files_to_merge
    subprocess.call(["python", scripts_path + "gdal_merge.py"] + params)


def gdalTranslate(input_file, out_file):
    print("Translating...")
    Io.deleteFile(out_file)
    params = [
        '-expand', 'rgb',
        '-co', 'PHOTOMETRIC=RGB',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=IF_NEEDED',
        input_file,
        out_file]
    subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalWarp(in_file, out_file):
    print("Warping...")
    Io.deleteFile(out_file)
    params = ['-s_srs', 'EPSG:27700',
              '-t_srs', 'EPSG:3857',
              '-co', 'PHOTOMETRIC=RGB',
              '-co', 'COMPRESS=DEFLATE',
              '-co', 'BIGTIFF=IF_NEEDED',
              in_file,
              out_file]
    subprocess.call([env_path + 'Library\\bin\\gdalwarp.exe'] + params)


def gdal2Tiles(in_file, out_dir, zoom):
    print("Tiling...")
    Io.deleteDirectory(out_dir)
    Io.makeDirectory(out_dir)
    params = [
        '-s', 'EPSG:3857',
        '--xyz',
        '-z', zoom,
        in_file,
        out_dir]
    subprocess.call(["python", scripts_path + 'gdal2tiles.py'] + params)
