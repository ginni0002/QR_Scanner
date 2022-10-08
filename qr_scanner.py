from cmath import e
from tkinter import E
import numpy as np
import cv2
import argparse as ap
import time
from pyzbar.pyzbar import decode

#global vars

contours = ""
img 	 = ""


def detect(path):
	# Decoding the qr code from a filtered image

	# loading image from path, applying filters and converting to edges.
	edges, blur = cvt_to_img(path)

	# After obtaining the edges, find contours and finally position markers.
	
	found_markers = find_contours(edges)

	# Create bounding boxes over the found markers
	# Can also pass a flag to draw contours.
	marker_boxes = Create_bboxes(found_markers,True)

	#find the center of qr code box, crop the qr code and create a bounding box over it.
	cropped_qr = crop_qr(marker_boxes, blur)

	try:
		decoded_string = decode(cropped_qr) # returns an array of qr codes, but we are only interested in one.

	except:
		return None

	return decoded_string




def cvt_to_img(path):

	"""
	read path to image and apply appropriate filters and edge detection.
	input argument(s):
		path - type(string)

	Output:
		8-bit Image same size as input image.
	"""
	try:
		img = cv2.imread(path)
	except FileNotFoundError:
		print("File not Found, please specify the absolute file path")
		return None
	
	#image obtained, passing it through filters.
	try:

		gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray , (3,3) , 0)
		#canny edge detection for now , can look out for better algorithms in the future.
		edge = cv2.Canny(blur , 100 , 200)
	
	except :
		print("Error in defining the filter arguments")
		return None
	
	return edge, blur



def find_contours(edges):
	"""
	Finds contours in an image passed through an edge detection filter.
	Parses through contours and stores the ones that match position markers for a qr code.

	Input:
		Image containing edges
	
	Output:
		contours stored as an array of vector of points/coordinates.


	"""
	#find contours 
	contours, heirarchy = cv2.findContours(edges , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

	heirarchy = heirarchy[0]
	found = []	#represents the contours that have a min heirarchy of 5 shapes i.e. position markers.
	
	for i in range(len(contours)):
		k=i
		count = 0
		# the heirarchy is a list containing further lists depending if there are shapes embedded
		# in the first structure/contour , and if the recursion is till 5 shapes , then its a qr code edge.
		
		while heirarchy[k][2] != -1: # not a big while loop , max iterations is 6
			k = heirarchy[k][2]
			count += 1
			if count >= 5 :
				found.append(i)

	return found



def Create_bboxes(markers, draw_flag):
	"""
	Draws and Creates bounding boxes over the found position markers.

	Input:
		position markers for qr code and a flag to draw the qr codes.

	Output:
		numpy array of bounding boxes.
	"""

	if(draw_flag):
		for i in markers:
			cv2.drawContours(img, contours , i , (0,255,0) , 1)
	
	bbox = []
	# bounding box array storing coordinates of each boxed contour.
	for i in markers:
		(x,y,w,h) = cv2.boundingRect(contours[i])
		bbox.append([x,y,x+w,y+h])
	boxes = np.array(bbox)

	return boxes



def crop_qr(boxes,blur):
	"""
	Finding the border of resulting qr code and cropping the image.
	Resulting image contains only the qr code.
	
	Input:
		boxes - numpy array of bounding boxes
		blur  - image passed through gaussian blur filter.

	Output:
		cropped qr code image.
	"""

	# Taking min value of all coordinates of contour boxes

	left,top = np.min(boxes,axis=0)[:2]
	right,bottom = np.max(boxes,axis=0)[2:]

	# Here 0.3 is the scaling factor relative to width and height of image
	# this will eliminate any effects of skewing/distortion/rotation in the qr code that can affect the bounding box.

	w = 0.3*(right-left)
	h = 0.3*(bottom-top)
	left,right = int(left-w),int(right+w)
	top,bottom = int(top-h),int(bottom+h)
	
	# if bounding box runs outside the image then crop it till the image border.
	if(left<0):
		left = 0
	if(right > img.shape[1]):
		right = img.shape[1]
	if(top<0):
		top = 0
	if(bottom > img.shape[0]):
		bottom = img.shape[0]

	#display the bounding rectangle
	cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),2)
	crop = blur[top:bottom,left:right] # crop qr code from image passed through gaussian blur.
	