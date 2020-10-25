import glob
import os
import shutil


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
