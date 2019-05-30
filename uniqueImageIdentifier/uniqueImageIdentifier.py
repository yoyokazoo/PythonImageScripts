import sys
import os
import argparse
from ast import literal_eval
from PIL import Image as PImage

def loadImages(srcPath, imgSuffix):
	imagesList = os.listdir(srcPath)
	loadedImages = []
	for image in imagesList:
		if image.endswith(imgSuffix):
			img = PImage.open(srcPath + image)
			loadedImages.append(img)

	return loadedImages

def findUniquePixels(images):
	uniquePixels = []

	width = images[0].size[0]
	height = images[0].size[1]

	print("For image %s width = %d height = %d" % (images[0], width, height))
	for x in range(width):
		for y in range(height):
			pixelsSeenSoFar = {}
			pixelUnique = True

			for image in images:
				pixelBeingChecked = image.getpixel((x,y))
				#print(pixelBeingChecked)
				if pixelBeingChecked in pixelsSeenSoFar:
					pixelUnique = False
					break
				else:
					pixelsSeenSoFar[pixelBeingChecked] = True

			if pixelUnique:
				uniquePixels.append((x,y))

	return uniquePixels

def printPixel(pixel, images):
	print("Printing pixel {0}".format(pixel))
	for image in images:
		print("\t%s: %s" % (image, image.getpixel(pixel)))

def printUniquePixels(uniquePixels, images):
	print("Unique Pixels: %s" % uniquePixels)
	for pixel in uniquePixels:
		printPixel(pixel, images)

DEFAULT_SRC_IMAGE_PATH = "./source_images/"
DEFAULT_DEST_IMAGE_PATH = "./dest_images/"
DEFAULT_IMG_SUFFIX = ".png"

parser = argparse.ArgumentParser() 
parser.add_argument('-s', '--src', help="Path to source image directory, something like the default, ./source_images/", default=DEFAULT_SRC_IMAGE_PATH)
parser.add_argument('-i', '--img_suffix', help="Image suffix, something like the default, .png", default=DEFAULT_IMG_SUFFIX)
args = parser.parse_args()
print(args)

loadedImages = loadImages(args.src, args.img_suffix)
uniquePixels = findUniquePixels(loadedImages)

printUniquePixels(uniquePixels, loadedImages)
