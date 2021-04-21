import glob
import os
import shutil
from PIL import Image
from pathlib import Path

'''
Utility methods on IO. 
'''


def getFilesList(directory, file_ext='*.tif'):
    return glob.glob(directory + file_ext)


def getFilesString(directory):
    files = getFilesList(directory)
    return " ".join(files)


def copyFiles(src, dest, file_names=(), file_name_regex='*.t*'):
    file_names_without_ext = [os.path.splitext(name)[0] for name in file_names]

    for file_path in glob.glob(os.path.join(src, '**', file_name_regex), recursive=True):
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]

        if len(file_names_without_ext) == 0 or \
                file_name_without_ext in file_names_without_ext:
            new_path = os.path.join(dest, file_name)
            shutil.copy(file_path, new_path)


# regex - file name regex
def moveFiles(src, dest, regex=()):
    files = os.listdir(src)
    for file in files:
        if not regex:
            shutil.move(os.path.join(src, file), dest)
        else:
            for reg in regex:
                if file.startswith(reg):
                    shutil.move(os.path.join(src, file), dest)
                    break


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


def makeDirectories(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def getFilesCount(path):
    return len(os.listdir(path))


def mergeTiles(src_paths, dest, zoom):
    deleteDirectory(dest)
    makeDirectories(dest)

    for path in src_paths:
        for subdir, dirs, files in os.walk(path + str(zoom)):
            if len(files) != 0:
                for file in files:
                    file_path = os.path.join(subdir, file)
                    subdir_from_tiles = os.path.join(Path(subdir).parent.name, Path(subdir).name)
                    makeDirectories(dest + subdir_from_tiles)

                    file_dest_path = os.path.join(dest, subdir_from_tiles, file)
                    if os.path.isfile(file_dest_path):
                        im = Image.open(file_path)
                        im_dest = Image.open(file_dest_path)
                        if __countNonBlack(im_dest) < __countNonBlack(im):
                            shutil.copyfile(file_path, file_dest_path)
                    else:
                        shutil.copy(file_path, file_dest_path)


def __countNonBlack(img):
    bbox = img.getbbox()
    if not bbox: return 0
    return sum(img.crop(bbox)
               .point(lambda x: 255 if x else 0)
               .convert("L")
               .point(bool)
               .getdata())
