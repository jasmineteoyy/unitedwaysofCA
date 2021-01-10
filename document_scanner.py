# import the necessary packages
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
from matplotlib import pyplot as plt
import random
# import argparse
import cv2
import imutils
# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required = True,
# 	help = "Path to the image to be scanned")
# args = vars(ap.parse_args())

def document_scanner(filename):
	# load the image and compute the ratio of the old height
	# to the new height, clone it, and resize it
	image = cv2.imread(filename)
	ratio = image.shape[0] / 500.0
	orig = image.copy()
	image = imutils.resize(image, height = 500)
	# convert the image to grayscale, blur it, and find edges
	# in the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 23, 77)
	# show the original image and the edge detected image
	# print("STEP 1: Edge Detection")
	# cv2.imshow("Image", image)
	# cv2.imshow("Edged", edged)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	# loop over the contours
	valid = False
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01*peri, True)
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		screenCnt = approx
		# cv2.drawContours(image, [screenCnt], -1, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 1)
		if len(approx) == 4:
			valid = True
			break
	# show the contour (outline) of the piece of paper
	# print("STEP 2: Find contours of paper")
	# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
	# # cv2.imshow("Outline", image)
	# # cv2.waitKey(0)
	# # cv2.destroyAllWindows()
	if not valid:
		return image
	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	# show the original and scanned images
	# print("STEP 3: Apply perspective transform")
	# cv2.imshow("Original", imutils.resize(orig, height = 650))
	# cv2.imshow("Scanned", imutils.resize(warped, height = 650))
	# cv2.waitKey(0)
	return warped

def scan_image(path):
	image = document_scanner(path)
	dot = path.find(".")
	path = path[:dot] + "_scanned" + path[dot:]
	cv2.imwrite(path, image)
	return path

# in_folder = 'images'
# out_folder = 'scanned'
# in_paths = [f'{in_folder}/IMG_{i}.jpg' for i in range(7723, 7740)]
# in_paths.append(f'{in_folder}/IMG_8287.jpg')
# out_paths = [f'{out_folder}/IMG_{i}.jpg' for i in range(7723, 7740)]
# out_paths.append(f'{out_folder}/IMG_8287.jpg')
# # original_images = [cv2.imread(path) for path in in_paths]
# scanned_images = [document_scanner(path) for path in in_paths]
# # f, axarr = plt.subplots(len(paths), 2)

# for i in range(len(in_paths)):
# 	cv2.imwrite(
# 		out_paths[i], 
# 		scanned_images[i]
# 	)