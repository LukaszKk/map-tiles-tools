import getopt
import glob
import math
import operator
import os
import shutil
import subprocess
import sys
import functools

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageCms
from PIL import ImageChops

Image.MAX_IMAGE_PIXELS = None

src_dir = os.path.dirname(os.path.abspath(__file__))
env_path = 'C:\\Users\\obliczenia\\anaconda3\\envs\\geo2\\'
input_path = src_dir + '\\..\\input\\'
output_path = src_dir + '\\..\\output\\'
scripts_path = env_path + 'Scripts\\'

input_data_path = input_path + 'data\\'
output_data_path = output_path + 'data\\'
output_tmp_path = output_path + 'tmp\\'
output_tmp2_path = output_path + 'tmp2\\'
output_tiles_path = output_path + 'tiles\\'

input_25k = input_data_path + '25k\\'
input_25kTmp = input_data_path + '25kTmp\\'
input_250k = input_data_path + '250k\\'

output_merged_path = output_path + 'merged\\'
merged_file = output_merged_path + 'merged.tif'
warped_file = output_merged_path + 'warped.tif'
translated_file = output_merged_path + 'translated.tif'

input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'


def getFilesList(directory, file_ext='*.tif'):
    return glob.glob(directory + file_ext)


def getFilesString(directory):
    files = getFilesList(directory)
    return " ".join(files)


def copyFiles(src, dest, file_name_regex='*.t*', delete_dest_before_copy=True):
    print("Copying files...")
    if delete_dest_before_copy:
        deleteDirectory(dest)
    makeDirectory(dest)
    for file_path in glob.glob(os.path.join(src, '**', file_name_regex), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)


def deleteDirectory(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except FileNotFoundError:
        pass


def deleteFile(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def makeDirectory(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def profileToProfile(input_data, out_path):
    print("Profiling...")
    makeDirectory(out_path)
    files = getFilesList(input_data)
    for image in files:
        in_image = Image.open(image)

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc,
                                           outputMode='RGB', renderingIntent=ImageCms.INTENT_ABSOLUTE_COLORIMETRIC)
        file_name = image.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        out_im.save(out_path + file_name)


def translateIntoOneFile(input_data, out_path):
    deleteDirectory(out_path)
    makeDirectory(out_path)
    files = getFilesList(input_data)
    for file in files:
        file_name = file.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        params = [
            '-of', 'GTiff',
            '-ot', 'Byte',
            '-b', '1',
            '-b', '2',
            '-b', '3',
            # '-expand', 'rgb',
            # '-co', 'PHOTOMETRIC=CMYK',
            '-co', 'COMPRESS=DEFLATE',
            file,
            out_path + file_name
        ]
        subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalMerge(input_data, out_file, is_pct=False):
    print("Merging...")
    deleteDirectory(output_merged_path)
    makeDirectory(output_merged_path)
    files_to_merge = getFilesList(input_data)
    pct = []
    if is_pct:
        pct = ['-pct']
    params = pct + [
        '-of', 'GTiff',
        '-ot', 'Byte',
        # '-co', 'ALPHA=NO',
        # '-co', 'PHOTOMETRIC=RGB',
        '-co', 'COMPRESS=DEFLATE',
        # '-co', 'TILED=YES',
        '-o', out_file]
    params = params + files_to_merge
    subprocess.call(["python", scripts_path + "gdal_merge.py"] + params)


def gdalTranslate(input_file, out_file):
    print("Translating...")
    deleteFile(out_file)
    params = [
        '-of', 'GTiff',
        '-ot', 'Byte',
        '-b', '1',
        '-b', '2',
        '-b', '3',
        # '-expand', 'rgb',
        # '-co', 'PHOTOMETRIC=RGB',
        '-co', 'COMPRESS=DEFLATE',
        # '-co', 'TILED=YES',
        input_file,
        out_file]
    subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdalWarp(in_file, out_file):
    print("Warping...")
    deleteFile(out_file)
    params = ['-s_srs', 'EPSG:27700',
              '-t_srs', 'EPSG:3857',
              '-of', 'GTiff',
              # '-co', 'PHOTOMETRIC=RGB',
              '-co', 'COMPRESS=DEFLATE',
              # '-co', 'TILED=YES',
              in_file,
              out_file]
    subprocess.call([env_path + 'Library\\bin\\gdalwarp.exe'] + params)


def gdal2Tiles(in_file, zoom):
    print("Tiling...")
    deleteDirectory(output_tiles_path)
    makeDirectory(output_tiles_path)
    params = [
        '-s', 'EPSG:3857',
        '--xyz',
        '-z', zoom,
        in_file,
        output_tiles_path]
    subprocess.call(["python", scripts_path + 'gdal2tiles.py'] + params)


def root_mean_square_diff(img1, img2):
    dif = ImageChops.difference(img1, img2).histogram()
    return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h * (i ** 2), dif, range(256))) / (
            float(img1.size[0]) * img1.size[1]))


def equal(img1, img2, show_dif=False):
    diff = ImageChops.difference(img1, img2)

    if diff.getbbox():
        print("Images are different")
        diff.save(output_path + 'dif.png')
        if show_dif:
            plt.imshow(diff)
            plt.show()
    else:
        print("Images are the same")


def main(argv=None):
    print('Usage: python src\\Main.py [-k -z <zoom_levels>]')
    input_dir = input_250k
    zoom = '11'

    use_profile = False
    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = input_25kTmp
        if opt == '-z':
            zoom = arg

    warp_in_file = merged_file
    if use_profile:
        # copyFiles(src=input_dir, dest=output_tmp_path)
        # profileToProfile(input_data=output_tmp_path, out_path=output_tmp2_path)
        # copyFiles(src=output_tmp_path, dest=output_tmp2_path, file_name_regex="*.TFW", delete_dest_before_copy=False)
        translateIntoOneFile(input_data=output_tmp2_path, out_path=output_data_path)
        # deleteDirectory(path=output_tmp_path)
        # deleteDirectory(path=output_tmp2_path)
        gdalMerge(input_data=output_data_path, out_file=merged_file)
        gdalTranslate(input_file=merged_file, out_file=translated_file)
    else:
        copyFiles(src=input_dir, dest=output_data_path)
        gdalMerge(input_data=output_data_path, out_file=merged_file, is_pct=True)
        gdalTranslate(input_file=merged_file, out_file=translated_file)
        warp_in_file = translated_file
    # gdalWarp(in_file=warp_in_file, out_file=warped_file)
    # gdal2Tiles(in_file=warped_file, zoom=zoom)


def main2(argv=None):
    print('Usage: python src\\Main.py [-s]')
    show_dif = False
    opts, args = getopt.getopt(argv, 's')
    for opt, arg in opts:
        if opt == '-s':
            show_dif = True

    img_path = '11\\' + '987\\' + '622.png'
    # img_path = '13\\' + '3902\\' + '2476.png'

    img1_path = input_path + img_path
    img2_path = output_tiles_path + img_path
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')

    print(root_mean_square_diff(img1, img2))
    equal(img1, img2, show_dif)


if __name__ == '__main__':
    output_tiles_path = output_path + 'tiles\\'

    main(sys.argv[1:])
    # main2(sys.argv[1:])
