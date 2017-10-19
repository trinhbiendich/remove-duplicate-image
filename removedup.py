#!/usr/bin/python

import sys
from PIL import Image
import argparse
import os
from os import listdir
from os.path import isfile, join
import imghdr
import uuid

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
def tinhToanHamming(img1, img2):
    hash1 = avhash(img1)
    hash2 = avhash(img2)
    dist = hamming(hash1, hash2)
    return dist
def tinhToanPercent(img1, img2):
    dist = tinhToanHamming(img1, img2)
    percent = (64 - dist) * 100 / 64
    return percent
def layAnhNhoNhat(img1, img2):
    im1 = Image.open(img1)
    im2 = Image.open(img2)
    width1, height1 = im1.size
    width2, height2 = im2.size
    if width1 < width2:
        return img1
    else:
        return img2

if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required = True,
        help = "path to input images")
    ap.add_argument("-o", "--output", required = True,
        help = "output folder")
    ap.add_argument("-max", "--percentsame", required = False, default=90,
        help = "Max percent same value default 90%")
    args = vars(ap.parse_args())

    inputFolder = os.path.join(args["input"], '')
    outputFolder = os.path.join(args["output"], '')
    maxPercent = int(float(args["percentsame"]))
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    print "Input folder : ", inputFolder
    print "Output folder : ", outputFolder
    onlyfiles = []
    for f in listdir(inputFolder):
        fullPath = join(inputFolder, f)
        if isfile(join(inputFolder, f)) and imghdr.what(fullPath) != None:
            onlyfiles.append(f)
    for f in onlyfiles:
        fullPath = join(inputFolder, f)
        for f2 in onlyfiles:
            fullPath2 = join(inputFolder, f2)
            if os.path.exists(fullPath2) and os.path.exists(fullPath) and f != f2:
                percent = tinhToanPercent(fullPath, fullPath2)
                if(percent >= maxPercent):
                    #move to new folder
                    movePath = layAnhNhoNhat(fullPath, fullPath2)
                    filename, file_extension = os.path.splitext(movePath)
                    tmpName = str(uuid.uuid4())
                    newName = tmpName + file_extension
                    newPath = join(outputFolder, newName)
                    print "percent ", percent
                    os.rename(movePath, newPath)
    print "Done!!!"

