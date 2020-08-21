import getopt
import glob
import math
import operator
import os
import shutil
import subprocess
import sys

import ImageChops
import gdal2tiles
from PIL import Image
from PIL import ImageCms

sys.path.append('C:/Software/Anaconda3/envs/geo_py37/Scripts')
import gdal_merge

Image.MAX_IMAGE_PIXELS = None

src_dir = os.path.dirname(os.path.abspath(__file__))

input_path = src_dir + '/../input/'
output_path = src_dir + '/../output/'

input_data_path = input_path + 'data/'
output_data_path = output_path + 'data/'
output_tiles_path = output_path + 'tiles3/'

input_25k = input_data_path + '25k/'
input_250k = input_data_path + '250k/'

output_merged_path = output_path + 'merged/'
merged_file = output_merged_path + 'merged.tif'
warped_file = output_merged_path + 'warped.tif'
translated_file = output_merged_path + 'translated.tif'

input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'


def getFiles(directory):
    files = os.listdir(directory)
    return [directory + file for file in files]


def copy(src, dest):
    for file_path in glob.glob(os.path.join(src, '**', '*.tif'), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)


def deleteDirectoryWithContent(directory):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass


def makeDirectories():
    try:
        os.mkdir(output_data_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(output_merged_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(output_tiles_path)
    except FileExistsError:
        pass


def profileToProfile(data_path):
    files = getFiles(data_path)
    for image in files:
        in_image = Image.open(image)
        in_image = in_image.convert('CMYK')

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc, outputMode='RGB')
        out_im.save(image)


def gdalMerge(data_path):
    params = ['',
              '-o', merged_file,
              '-of', 'GTiff',
              '-pct',
              '-co', 'ALPHA=NO']
    files_to_merge = getFiles(data_path)
    params = params + files_to_merge
    gdal_merge.main(params)


def gdalWarp():
    params = ['-s_srs', 'EPSG:27700',
              '-t_srs', 'EPSG:3857',
              merged_file,
              warped_file]
    subprocess.run(['C:/Software/Anaconda3/envs/geo_py37/Library/bin/gdalwarp.exe'] + params)


def gdalTranslate():
    params = ['-of', 'GTiff',
              '-expand', 'rgb',
              warped_file,
              translated_file]
    subprocess.run(['C:/Software/Anaconda3/envs/geo_py37/Library/bin/gdal_translate.exe'] + params)


def gdal2Tiles(zoom):
    gdal2tiles.generate_tiles(translated_file,
                              output_tiles_path,
                              zoom=zoom,
                              s_srs='EPSG:3857')


def root_mean_square_diff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(
        reduce(operator.add, map(lambda h, i: h * (i ** 2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

def main(argv=None):
    opts, args = getopt.getopt(argv, 'k')
    input_dir = input_250k

    deleteDirectoryWithContent(output_data_path)
    makeDirectories()
    use_profile = False

    for opt, arg in opts:
        if opt == '-k':
            use_profile = True
            input_dir = input_25k

    copy(input_dir, output_data_path)

    if use_profile:
        profileToProfile(output_data_path)
    gdalMerge(output_data_path)
    gdalWarp()
    gdalTranslate()
    gdal2Tiles('7-10')


if __name__ == '__main__':
    main(sys.argv[1:])
