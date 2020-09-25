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
env_path = 'D:\\Software\\Anaconda3\\envs\\geo2\\'
input_path = src_dir + '\\..\\input\\'
output_path = src_dir + '\\..\\output\\'
scripts_path = env_path + 'Scripts\\'

input_data_path = input_path + 'data\\'
output_data_path = output_path + 'data\\'
output_tmp_path = output_path + 'tmp\\'
output_tiles_path = output_path + 'tiles\\'

input_25k = input_data_path + '25k\\'
input_250k = input_data_path + '250k\\'

output_merged_path = output_path + 'merged\\'
merged_file = output_merged_path + 'merged.tif'
warped_file = output_merged_path + 'warped.tif'
translated_file = output_merged_path + 'translated.vrt'

input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'


def getFilesList(directory):
    return glob.glob(directory + '*.tif')


def getFilesString(directory):
    files = getFilesList(directory)
    return " ".join(files)


def copyFiles(src, dest, regex='*.t*', delete_content=True):
    print("Copying files...")
    if delete_content:
        deleteDirectoryWithContent(dest)
    makeDirectory(dest)
    for file_path in glob.glob(os.path.join(src, '**', regex), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)


def deleteDirectoryWithContent(path):
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


def profileToProfile(data_path, out_path):
    print("Profiling...")
    makeDirectory(out_path)
    files = getFilesList(data_path)
    for image in files:
        in_image = Image.open(image)

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc, outputMode='RGB')
        file_name = image.split('\\')
        file_name_len = len(file_name)
        file_name = file_name[file_name_len - 1]
        out_im.save(out_path + file_name)


def gdalMerge(data_path):
    print("Merging...")
    deleteDirectoryWithContent(output_merged_path)
    makeDirectory(output_merged_path)
    files_to_merge = getFilesList(data_path)
    params = ['-pct',
              '-of', 'GTiff',
              '-co', 'ALPHA=NO',
              '-o', merged_file]
    params = params + files_to_merge
    subprocess.call(["python", scripts_path + "gdal_merge.py"] + params)


def gdalWarp():
    print("Warping...")
    deleteFile(warped_file)
    params = ['-s_srs', 'EPSG:27700',
              '-t_srs', 'EPSG:3857',
              '-of', 'GTiff',
              merged_file,
              warped_file]
    subprocess.call([env_path + 'Library\\bin\\gdalwarp.exe'] + params)


def gdalTranslate():
    print("Translating...")
    deleteFile(translated_file)
    params = ['-of', 'vrt',
              '-expand', 'rgba',
              warped_file,
              translated_file]
    subprocess.call([env_path + 'Library\\bin\\gdal_translate.exe'] + params)


def gdal2Tiles(zoom):
    print("Tiling...")
    deleteDirectoryWithContent(output_tiles_path)
    makeDirectory(output_tiles_path)
    params = ['-s', 'EPSG:3857',
              '--xyz',
              '-z', zoom,
              translated_file,
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
    zoom = '13'

    use_profile = False
    opts, args = getopt.getopt(argv, 'kz:')
    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = input_25k
        if opt == '-z':
            zoom = arg

    if use_profile:
        copyFiles(input_dir, output_tmp_path)
        profileToProfile(output_tmp_path, output_data_path)
        copyFiles(output_tmp_path, output_data_path, "*.TFW", False)
        deleteDirectoryWithContent(output_tmp_path)
    else:
        copyFiles(input_dir, output_data_path)
    gdalMerge(output_data_path)
    gdalWarp()
    gdalTranslate()
    gdal2Tiles(zoom)


def main2(argv=None):
    print('Usage: python src\\Main.py [-s]')
    show_dif = False
    opts, args = getopt.getopt(argv, 's')
    for opt, arg in opts:
        if opt == '-s':
            show_dif = True

    img_path = '11\\' + '987\\' + '622.png'
    # img_path = '13\\' + '3902\\' + '2476.png'

    img1_path = input_data_path + img_path
    img2_path = output_tiles_path + img_path
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')

    print(root_mean_square_diff(img1, img2))
    equal(img1, img2, show_dif)


if __name__ == '__main__':
    output_tiles_path = output_path + 'tiles\\'

    main(sys.argv[1:])
    # main2(sys.argv[1:])
