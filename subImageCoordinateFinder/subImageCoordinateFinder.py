import sys
import os
import argparse
from ast import literal_eval
from PIL import Image as PImage

def loadDirectoryOfImages(srcPath, imgSuffix):
	images = []

	imagePaths = os.listdir(srcPath)
	for imagePath in imagePaths:
		if imagePath.endswith(imgSuffix):
			image = PImage.open(srcPath + imagePath)
			images.append(image)

	return images

def searchForSubImages(sourcePath, searchPath, imgSuffix):
	imagesToBeFound = loadDirectoryOfImages(sourcePath, imgSuffix)
	imagesToBeSearched = loadDirectoryOfImages(searchPath, imgSuffix)

	for searchImage in imagesToBeSearched:
		for findImage in imagesToBeFound:
			print("Searching {0} for {1}".format(searchImage.filename, findImage.filename))
			for searchX in range(searchImage.size[0]):
				for searchY in range(searchImage.size[1]):

					# check that full search image could even fit
					if (searchX + findImage.size[0] > searchImage.size[0]) or (searchY + findImage.size[1] > searchImage.size[1]):
						break

					allPixelsMatch = True
					for findX in range(findImage.size[0]):
						for findY in range(findImage.size[1]):

							searchPixel = searchImage.getpixel((searchX + findX, searchY + findY))
							findPixel = findImage.getpixel((findX, findY))
							#print("searchX = {0}, searchY = {1}, findX = {2}, findY = {3}, searchPixel = {4}, findPixel = {5}".format(searchX, searchY, findX, findY, searchPixel, findPixel))
							if searchPixel != findPixel:
								#print("Pixels don't match, moving on")
								allPixelsMatch = False
								break

						if not allPixelsMatch:
							#print("Not all pixels match, breaking")
							break

					if allPixelsMatch:
						print("Found subImage {0} in searchImage {1} at {2}".format(findImage.filename, searchImage.filename, (searchX, searchY)))

DEFAULT_SRC_IMAGE_PATH = "./source_images/"
DEFAULT_SEARCH_IMAGE_PATH = "./search_images/"
DEFAULT_IMG_SUFFIX = ".png"

parser = argparse.ArgumentParser() 
parser.add_argument('-s', '--src', help="Path to source image directory, something like the default, ./source_images/", default=DEFAULT_SRC_IMAGE_PATH)
parser.add_argument('-c', '--search', help="Path to search image directory, something like the default, ./search_images/", default=DEFAULT_SEARCH_IMAGE_PATH)
parser.add_argument('-i', '--img_suffix', help="Image suffix, something like the default, .png", default=DEFAULT_IMG_SUFFIX)
args = parser.parse_args()
print(args)

if not (args.src[-1] == "/" or args.src[-1] == "\\"):
	args.src = args.src + "/"
if not (args.search[-1] == "/" or args.search[-1] == "\\"):
	args.search = args.search + "/"

searchForSubImages(args.src, args.search, args.img_suffix)

print("All images searched.")