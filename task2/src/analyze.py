import sys
import math
from timeit import default_timer as timer
from PIL import Image


#	analyze.py
#	functions for calculating the color layout descriptor


def loadImage( path ):
	#
	#	loads the image and returns it
	#
	try:
		image = Image.open(path)
	except IOError:
		print("cannot open", path)
		quit()

	return image


def shrinkImage( image ):
	#
	#	divides the image in 8x8 blocks and scales down
	#	using the average color of these blocks
	#
	smallImage = Image.new(image.mode, (8,8))
	pixelsNew = smallImage.load()
	pixels = image.load()

	x = int(image.width/8)
	y = int(image.height/8)

	# going through all blocks
	for i in range(8):
		for j in range (8):
			pixelBlockRed = []
			pixelBlockBlue = []
			pixelBlockGreen = []
			for k in range(i*x, i*x+x):
				for l in range(j*y, j*y+y):					
					r,g,b = pixels[k,l]
					pixelBlockRed.append(r)
					pixelBlockGreen.append(g)
					pixelBlockBlue.append(b)
			# average the colors and save to new image
			pixelsNew[i,j] = (int(sum(pixelBlockRed)/len(pixelBlockRed)),int(sum(pixelBlockGreen)/len(pixelBlockGreen)),int(sum(pixelBlockBlue)/len(pixelBlockBlue)))

	return smallImage 


def convertToYCbCr( image ):
	#
	#	converts to YCbCr Colorspace
	#
	image.convert("RGB") #image.convert("YCbCr") seems not to work, would be much easier
	pixels = image.load()

	for i in range(image.size[0]):
		for j in range (image.size[1]):
			r,g,b = pixels[i,j]			
			# using the YCbCr transformation matrix
			y = int(round(0 +0.299*r + 0.587*g + 0.114*b))
			cb = int(round(128 -0.168736*r -0.331364*g + 0.5*b))
			cr = int(round(128 +0.5*r - 0.418688*g - 0.081312*b))
			pixels[i,j] = (y, cb, cr)	
	return image


def dctTransformation(image):
	#
	# 	does the DCT transformation and quantizes the result
	# 	returns the descriptor

	# alpha-function
	def alpha( p , N):
			if p == 0:
				return math.sqrt(1/N)
			else:
				return math.sqrt(2/N)	

	# function to calcuate one coefficient
	def ac ( image, channel, u, v, N):
		sumresult = 0
		pixels = image.load()
		for x in range(N):
			for y in range(N):
				sumresult += pixels[x,y][channel] * math.cos((math.pi*(2*x+1)*u)/(2*N)) * math.cos((math.pi*(2*y+1)*v)/(2*N))
		return alpha(u, N) * alpha(v, N) * sumresult

	N = 8 # number of blocks, in our case always 8
	
	# resulting coefficients
	yDC = 0
	cbDC = 0
	crDC = 0
	yCoeffs = []
	cbCoeffs = []
	crCoeffs = []

	# using zig-zag to get all needed coefficients
	# also quantize DC: 6 Bit=64 , AC: 5 Bit=32

	yDC = round(ac(image, 0, 0, 0, N)/64)
	yCoeffs.append(round(ac(image, 0, 0, 1, N)/32)) #2
	yCoeffs.append(round(ac(image, 0, 1, 0, N)/32)) #9
	yCoeffs.append(round(ac(image, 0, 2, 0, N)/32)) #17
	yCoeffs.append(round(ac(image, 0, 1, 1, N)/32)) #10
	yCoeffs.append(round(ac(image, 0, 0, 2, N)/32)) #3

	cbDC = round(ac(image, 1, 0, 0, N)/64)
	cbCoeffs.append(round(ac(image, 1, 0, 1, N)/32)) #2
	cbCoeffs.append(round(ac(image, 1, 1, 0, N)/32)) #9

	crDC = round(ac(image, 2, 0, 0, N)/64)
	crCoeffs.append(round(ac(image, 2, 0, 1, N)/32)) #2
	crCoeffs.append(round(ac(image, 2, 1, 0, N)/32)) #9

	return yDC, yCoeffs, cbDC, cbCoeffs, crDC, crCoeffs


def createDescriptor( filename ):
	#
	# calculate the descriptor by following the algorithm
	#
	return dctTransformation(convertToYCbCr(shrinkImage(loadImage(filename))))