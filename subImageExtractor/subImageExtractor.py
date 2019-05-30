import sys
import os
import argparse
from ast import literal_eval
from PIL import Image as PImage

def cropImages(srcPath, destPath, imgSuffix, tupleList):
	# clear out the dest directory of any images, so user can re-run indiscriminately
	for subDir, dirs, files in os.walk(destPath):
		for fileName in files:
			if fileName.endswith(imgSuffix):
				os.remove(os.path.join(subDir, fileName))

	imagesList = os.listdir(srcPath)
	for image in imagesList:
		if image.endswith(imgSuffix):
			img = PImage.open(srcPath + image)
			for index in range(len(tupleList)):
				cropTuple = tupleList[index]
				newImg = img.crop(cropTuple)
				newImg.save(destPath + str(index) + "_" + image)

DEFAULT_SRC_IMAGE_PATH = "./source_images/"
DEFAULT_DEST_IMAGE_PATH = "./dest_images/"
DEFAULT_IMG_SUFFIX = ".png"

parser = argparse.ArgumentParser() 
parser.add_argument('-s', '--src', help="Path to source image directory, something like the default, ./source_images/", default=DEFAULT_SRC_IMAGE_PATH)
parser.add_argument('-d', '--dest', help="Path to destination image directory, something like the default, ./dest_images/", default=DEFAULT_DEST_IMAGE_PATH)
parser.add_argument('-i', '--img_suffix', help="Image suffix, something like the default, .png", default=DEFAULT_IMG_SUFFIX)
parser.add_argument('-c', '--crops',help="Any number of 4-tuples which specify the top,left,width,height and bottom-right coordinates, something like '-c (0,0,100,100) (100,100,100,100)'",  nargs='*', required=True)
args = parser.parse_args()
print(args)

tupleList = []
# a little scrappy
for stringTuple in args.crops:
	actualTuple = literal_eval(stringTuple)
	# crop takes top/left bottom/right, which isn't as convenient as top/left width/height, especially when extracting a repeating pattern in an image
	cropTuple = (actualTuple[0], actualTuple[1], actualTuple[0] + actualTuple[2], actualTuple[1] + actualTuple[3])
	tupleList.append(cropTuple)

if not (args.dest[-1] == "/" or args.dest[-1] == "\\"):
	args.dest = args.dest + "/"

# create dest directory, if necessary
if not os.path.isdir(args.dest):
		os.mkdir(args.dest);

cropImages(args.src, args.dest, args.img_suffix, tupleList)

print("All images cropped.")