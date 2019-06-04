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

def printPixel(pixel, images):
	print("Printing pixel {0}".format(pixel))
	for imagePath in images:
		print("\t%s:\t%s" % (imagePath, images[imagePath].getpixel(pixel)))

def printUniquePixels(uniquePixels, images):
	print("Unique Pixels: %s" % uniquePixels)
	for pixel in uniquePixels:
		printPixel(pixel, images)

def getPixelFrequency(pixel, images):
	pixelFrequency = {}
	for imagePath in images:
		image = images[imagePath]
		pixelValue = image.getpixel(pixel)
		#print("Pixel value = {0} for image {1}".format(pixelValue, imagePath))
		if not pixelValue in pixelFrequency:
			pixelFrequency[pixelValue] = 1
		else:
			pixelFrequency[pixelValue] += 1

	return pixelFrequency

def printPixelFrequency(pixel, images):
	pixelFrequency = getPixelFrequency(pixel, images)
	print("Pixel frequency for {0}:".format(pixel))
	for pixelValue in pixelFrequency:
		print("\tFrequency of {0} = {1}".format(pixelValue, pixelFrequency[pixelValue]))

def findUniquePixels(images):
	uniquePixels = {}

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

	completeUniquenessFound = False
	roundNum = 0



	while(len(images) > 0):
		roundNum += 1
		minPixelUniqueness = 100000 # math.max
		mostUniquePixel = None
		for x in range(width):
			for y in range(height):
				pixelTuple = (x,y)
				pixelsSeenSoFar = {}
				pixelDupeCount = 0
				dupes = {}

				for imagePath in images:
					image = images[imagePath]
					pixelBeingChecked = image.getpixel(pixelTuple)

					if(pixelTuple in uniquePixels and uniquePixels[pixelTuple][2] == imagePath):
						#print("Pixel being checked is a 'unique pixel' {0}, stored val is {1}, my val is {2} ({3}).  Skipping.".format(pixelTuple, uniquePixels[pixelTuple], pixelBeingChecked, imagePath))
						#print("Skipping already unique pixel {0}".format(pixelTuple))
						continue

					if pixelBeingChecked in pixelsSeenSoFar:
						#if pixelDupeCount >= minPixelUniqueness:
						#	print("Dupe found, perhaps new minPixelUniqueness?! Pixel = {0}, {1}, {2}".format(pixelTuple, pixelBeingChecked, imagePath))
						pixelDupeCount += 1
						if not pixelTuple in dupes:
							dupes[pixelTuple] = []
						dupes[pixelTuple].append(imagePath)
					else:
						#print("First pixel seen for {0} = {1} ({2})".format(pixelTuple, pixelBeingChecked, imagePath))
						pixelsSeenSoFar[pixelBeingChecked] = True

				if pixelDupeCount < minPixelUniqueness and pixelTuple not in uniquePixels:
					#print("Pixel dupe count for pixel {0} = {1}.  Dupes = {2}".format(pixelTuple, pixelDupeCount, dupes))
					minPixelUniqueness = pixelDupeCount
					mostUniquePixel = (pixelTuple, pixelBeingChecked, imagePath)

		print("After round {0}, mostUniquePixel = {1}".format(roundNum, mostUniquePixel))
		uniquePixels[mostUniquePixel[0]] = mostUniquePixel

		# remove all images from list that have a freq of 1 for that pixel
		# (theoretically we could hit this with a lowest freq >1, but that means there's an identical
		# image in the directory, which I'll deal with later (no real use case))

		# since this is more of a preprocessing tool than a runtime tool I haven't focused
		# on performance but if that becomes a concern this could probably be cleaned up
		pixelFrequency = getPixelFrequency(mostUniquePixel[0], images)
		printPixelFrequency(mostUniquePixel[0], images)
		culledImages = {}
		for imagePath in images:
			image = images[imagePath]
			if not pixelFrequency[image.getpixel(mostUniquePixel[0])] == 1:
				culledImages[imagePath] = image

		images = culledImages

	return uniquePixels

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

# TODO: add this if useful -- either look for the largest minimum color distance (avoids issue where "unique" pixel is two shades of grey that are very close etc.)
# or look for highest average color distance away from eachother
#pixelUniquenessScores = findPixelUniquenessScores(uniquePixels, loadedImages)

#printPixelFrequency((9,8), loadedImages)
#printUniquePixels(uniquePixels, loadedImages)
