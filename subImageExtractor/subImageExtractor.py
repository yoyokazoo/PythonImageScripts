from os import listdir
from PIL import Image as PImage

def cropImages(src_path, dest_path, tupleArray):
	# return array of images

	imagesList = listdir(src_path)
	loadedImages = []
	for image in imagesList:
		if image[0] != ".":
			img = PImage.open(src_path + image)
			loadedImages.append(img)

			for arrayIndex in range(len(tupleArray)):
				cropTuple = tupleArray[arrayIndex]
				newImg = img.crop(cropTuple)
				newImg.save(dest_path + str(arrayIndex) + "_" + image)

	return loadedImages

SRC_IMAGE_PATH = "./source_images/"
DEST_IMAGE_PATH = "./dest_images/"

firstTuple = (2888, 329, 2888 + 31, 329 + 44)
secondTuple = (2924, 329, 2924 + 31, 329 + 44)

tupleArray = [firstTuple, secondTuple]

cropImages(SRC_IMAGE_PATH, DEST_IMAGE_PATH, tupleArray)