#!/usr/bin/python
#python removedup.py -i pics -o imgs

import sys
from PIL import Image
import argparse
import os
from os import listdir
from os.path import isfile, join, abspath
import imghdr
import uuid
import shutil

class FileItem:
    def __init__(self):
        self.path = ""
        self.name = ""
        self.ext = ""
        self.h = ""
        self.width = 0
        self.height = 0
    def __init__(self, name, ext, path, hash1, width, height):
        self.path = path
        self.name = name
        self.ext = ext
        self.h = hash1
        self.width = width
        self.height = height
    def __repr__(self):
        return " \n\n======== FileItem with filename:%s ========\npath:%s \nhash:%d \n%dx%d" % (self.name, 
                self.path, self.h, self.width, self.height)

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h
def tinhToanHamming(item1, item2):
    dist = hamming(item1.h, item2.h)
    return dist
def tinhToanPercent(item1, item2):
    dist = tinhToanHamming(item1, item2)
    percent = (64 - dist) * 100 / 64
    return percent
def layItemCoKichThuocNhoHon(item1, item2):
    if item1.width < item2.width:
        return item1
    else:
        return item2

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required = True,
        help = "path to input images")
    ap.add_argument("-o", "--output", required = True,
        help = "output folder")
    ap.add_argument("-max", "--percentsame", required = False, default=95,
        help = "Max percent same value default 95%")
    args = vars(ap.parse_args())

    #Define variable
    inputFolder = abspath(os.path.join(args["input"], ''))
    outputFolder = abspath(os.path.join(args["output"], ''))
    notImgFolder = join(outputFolder, "not_img")
    maxPercent = int(float(args["percentsame"]))
    objs = []

    #create folder if it not exists
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    if not os.path.exists(notImgFolder):
        os.makedirs(notImgFolder)

    #Print for view
    print "Input folder : ", inputFolder
    print "Output folder : ", outputFolder

    valid_images = [".jpg",".png", ".jpeg"]
    for path, subdirs, files in os.walk(inputFolder):
        for f in files:
            fullPath = join(path, f)
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                notImgPath = join(notImgFolder, f)
                if os.path.exists(notImgPath):
                    tmpName = str(uuid.uuid4())
                    newName = tmpName + ext
                    notImgPath = join(notImgFolder, newName)
                shutil.move(fullPath, notImgPath)
                continue
            if imghdr.what(fullPath) != None:
                img = Image.open(fullPath)
                width, height = img.size
                hash1 = avhash(img)
                obj = FileItem(f, ext, fullPath, hash1, width, height)
                objs.append(obj)
            else:
                notImgPath = join(notImgFolder, f)
                if os.path.exists(notImgPath):
                    tmpName = str(uuid.uuid4())
                    newName = tmpName + ext
                    notImgPath = join(notImgFolder, newName)
                shutil.move(fullPath, notImgPath)

    for item1 in objs:
        for item2 in objs:
            if not os.path.exists(item1.path) or not os.path.exists(item2.path) or item1.path == item2.path:
                continue
            percent = tinhToanPercent(item1, item2)
            if(percent >= maxPercent):
                #move to new folder
                item = layItemCoKichThuocNhoHon(item1, item2)
                tmpName = str(uuid.uuid4())
                newPath = join(outputFolder, item.name)
                if os.path.exists(newPath):
                    newName = tmpName + item.ext
                    newPath = join(outputFolder, newName)
                print "percent ", percent, " - ", item.name
                shutil.move(item.path, newPath)
    print "Done!!!"

