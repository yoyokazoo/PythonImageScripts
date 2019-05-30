import sys
import os
import argparse
from ast import literal_eval
from PIL import Image as PImage

def loadImages(srcPath, imgSuffix):
	imagesList = os.listdir(srcPath)
	loadedImages = {}
	for image in imagesList:
		if image.endswith(imgSuffix):
			img = PImage.open(srcPath + image)
			loadedImages[image] = img

	return loadedImages

def findUniquePixels(images):
	uniquePixels = []

	width = -1
	height = -1
	firstImage = ""
	for imagePath in images:
		image = images[imagePath]
		if width == -1 and height == -1:
			width = image.size[0]
			height = image.size[1]
			firstImage = imagePath

		if width != image.size[0] or height != image.size[1]:
			raise Exception("Not all images are the same width height! Found both {0},{1} ({4}) and {2},{3} ({5})".format(width, height, image.size[0], image.size[1], firstImage, imagePath))

	for x in range(width):
		for y in range(height):
			pixelsSeenSoFar = {}
			pixelUnique = True

			for image in images.values():
				pixelBeingChecked = image.getpixel((x,y))
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
	for imagePath in images:
		print("\t%s:\t%s" % (imagePath, images[imagePath].getpixel(pixel)))

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
#pixelUniquenessScores = findPixelUniquenessScores(uniquePixels, loadedImages)

printUniquePixels(uniquePixels, loadedImages)
