from PIL import Image
from PIL import ImageCms
import sys
import os
import subprocess
import gdal2tiles
sys.path.append('C:/Software/Anaconda3/envs/geo_py37/Scripts')
import gdal_merge


src_dir = os.path.dirname(os.path.abspath(__file__))

input_path = src_dir + '/../input/'
output_path = src_dir + '/../output/'

input_data_path = input_path + 'data/'
output_data_path = output_path + 'data/'
output_tiles_path = output_path + 'tiles2/'

input_25k = input_data_path + '25k/'
input_250k = input_data_path + '250k/'

merged_file = output_path + 'merged/' + 'merged.tif'
warped_file = output_path + 'merged/' + 'warped.tif'
translated_file = output_path + 'merged/' + 'translated.tif'

input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'

files = os.listdir(input_250k)
files = [input_250k + file for file in files]


def profileToProfile():
    for image in files:
        in_image = Image.open(image)
        in_image = in_image.convert("CMYK")

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc, outputMode='RGB')

        filename = image.split('/')
        out_im.save(output_data_path + filename[len(filename) - 1].split('.')[0] + ".tif")


def gdalMerge():
    params = ['',
              '-o', merged_file,
              '-of', 'GTiff',
              '-pct',
              '-co', 'ALPHA=NO']
    files_to_merge = os.listdir(output_data_path)
    files_to_merge = [output_data_path + file for file in files_to_merge]
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
              '-expand', 'rgba',
              warped_file,
              translated_file]
    subprocess.run(['C:/Software/Anaconda3/envs/geo_py37/Library/bin/gdal_translate.exe'] + params)


def gdal2Tiles():
    gdal2tiles.generate_tiles(translated_file,
                              output_tiles_path,
                              zoom='11-12',
                              s_srs='EPSG:3857')


# parametr funkcji 50k zmienic rozszerzenie z tfw na pgw
# 250k - ominac profiletoprofile
# zmienic uklad wsp przed generate_tiles
# na zmergowanym tiffie generate_tiles i podac 3857 w srs
# gdal_translate
# 27700 - sprawdzic
# 3857 - sprawdzic


def main():
    print()
    profileToProfile()
    gdalMerge()
    # gdalWarp()
    # gdalTranslate()
    # gdal2Tiles()


if __name__ == '__main__':
    main()

