from PIL import Image
from PIL import ImageCms
import sys
import os
import gdal2tiles

sys.path.append('C:/Software/Anaconda3/envs/geo_py37/Scripts')
import gdal_merge as gm

src_dir = os.path.dirname(os.path.abspath(__file__))
input_path = src_dir + '/../input/'
output_path = src_dir + '/../output/'
input_data_path = input_path + 'data/'
input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'

files = os.listdir(input_data_path)


def profile_to_profile():
    images = [input_data_path + file for file in files]

    for image in images:
        in_image = Image.open(image)
        in_image = in_image.convert("CMYK")

        out_im = ImageCms.profileToProfile(in_image, inputProfile=input_icc, outputProfile=output_icc, outputMode='RGB')

        filename = image.split('/')
        out_im.save(output_path + filename[len(filename) - 1].split('.')[0] + ".png")


# profile_to_profile()
# gdal2tiles.generate_tiles(output_path + "HP.png", output_path + "data", profile="raster", zoom='11-12',
#                           s_srs="ESPG:xyz")

params = ['', '-o', output_path + 'merged/' + 'merged.tif']
params = params + [input_data_path + file for file in files]
gm.main(params)
