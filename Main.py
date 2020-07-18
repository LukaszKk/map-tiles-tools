from PIL import ImageCms
from PIL import Image
import PIL
import os
import io

input_path = 'input/'
input_data_path = input_path + 'data/'
files = os.listdir(input_data_path)
input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
output_icc = input_path + 'sRGB_v4_ICC_preference.icc'

images = [Image.open(input_data_path + file, mode='r') for file in files]



# im = im.convert('CMYK')
# print(im.mode)

# transform = ImageCms.buildTransform(input_icc, output_icc, 'CMYK', 'RGB')
# ImageCms.applyTransform(im, transform)

# out_im = ImageCms.profileToProfile(im, inputProfile=input_icc, outputProfile=output_icc, outputMode='RGB')
# print(out_im.mode)
# out_im.show()


