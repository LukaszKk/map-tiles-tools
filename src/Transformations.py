import subprocess

from PIL import Image
from PIL import ImageCms

import IOperations as Io
from PathProvider import PathProvider


Image.MAX_IMAGE_PIXELS = None


def profileToProfile(input_data, out_path):
    files = Io.getFilesList(input_data)
    for image in files:
        in_image = Image.open(image)

        out_im = ImageCms.profileToProfile(im=in_image,
                                           inputProfile=PathProvider.input_icc,
                                           outputProfile=PathProvider.output_icc,
                                           outputMode='RGB')
        file_name = image.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        out_im.save(out_path + file_name)


def translateIntoOneFile(input_data, out_path):
    files = Io.getFilesList(input_data)
    for file in files:
        file_name = file.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        params = [
            '-b', '1',
            '-b', '2',
            '-b', '3',
            '-a_srs', 'EPSG:27700',
            '-of', 'GTiff',
            '-ot', 'Byte',
            '-co', 'PHOTOMETRIC=RGB',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'BIGTIFF=YES',
            file,
            out_path + file_name
        ]
        subprocess.call([PathProvider.env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalMerge(input_data, out_file, is_pct=False):
    files_to_merge = Io.getFilesList(input_data)
    if is_pct:
        additional_options = ['-pct']
    else:
        additional_options = ['-co', 'PHOTOMETRIC=RGB']
    params = additional_options + [
        '-ot', 'Byte',
        '-of', 'GTiff',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=YES',
        '-o', out_file
        ]
    params = params + files_to_merge
    subprocess.call(["python", PathProvider.scripts_path + "gdal_merge.py"] + params)


def gdalTranslate(input_file, out_file):
    params = [
        '-ot', 'Byte',
        '-of', 'GTiff',
        '-expand', 'rgb',
        '-co', 'PHOTOMETRIC=RGB',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=YES',
        input_file,
        out_file]
    subprocess.call([PathProvider.env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalWarp(in_file, out_file):
    Io.deleteFile(out_file)
    params = [
        '-ot', 'Byte',
        '-of', 'GTiff',
        '-t_srs', 'EPSG:3857',
        '-co', 'PHOTOMETRIC=RGB',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'BIGTIFF=YES',
        in_file,
        out_file]
    subprocess.call([PathProvider.env_path + 'Library\\bin\\gdalwarp.exe'] + params)


def gdal2Tiles(in_file, out_dir, zoom):
    params = [
        '-s', 'EPSG:3857',
        '-a', '0',
        '-z', zoom,
        '--xyz',
        in_file,
        out_dir]
    subprocess.call(["python", PathProvider.scripts_path + 'gdal2tiles.py'] + params)
