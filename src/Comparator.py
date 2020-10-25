import math
import operator
import functools
import getopt
import os

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageChops

src_dir = os.path.dirname(os.path.abspath(__file__))
input_path = src_dir + '\\..\\input\\'
output_path = src_dir + '\\..\\output\\'


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


def main(out_dir, argv):
    print('Usage: python src\\Main.py [-s]')
    show_dif = False
    opts, args = getopt.getopt(argv, 's')
    for opt, arg in opts:
        if opt == '-s':
            show_dif = True

    # img_path = '11\\' + '987\\' + '622.png'
    img_path = '13\\' + '3902\\' + '2472.png'

    img1_path = input_path + img_path
    img2_path = out_dir + img_path
    img1 = Image.open(img1_path).convert('RGBA')
    img2 = Image.open(img2_path).convert('RGBA')

    print(root_mean_square_diff(img1, img2))
    equal(img1, img2, show_dif)