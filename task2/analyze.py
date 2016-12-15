import sys
import math
from timeit import default_timer as timer
from PIL import Image


#	analyze.py
#
#	usage: python3 analyze.py example.jpg


def loadImage( path ):
	#
	#	loads the image and returns it
	#
	try:
		image = Image.open(path)
	except IOError:
		print("cannot open", path)
		quit()

	#print(path, "(", image.width, "x", image.height, ") loaded")
	return image


def shrinkImage( image ):
	#
	#	divides the image in 8x8 blocks and scales down
	#
	smallImage = Image.new(image.mode, (8,8))
	pixelsNew = smallImage.load()
	pixels = image.load()

	x = int(image.width/8)
	y = int(image.height/8)

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
			pixelsNew[i,j] = (int(sum(pixelBlockRed)/len(pixelBlockRed)),int(sum(pixelBlockGreen)/len(pixelBlockGreen)),int(sum(pixelBlockBlue)/len(pixelBlockBlue)))

	#image.resize((8,8),Image.ANTIALIAS).resize((64,64),Image.NEAREST).show()

	return smallImage # image.resize((8,8),Image.ANTIALIAS) # resize same result as average downsampling??


def convertToYCbCr( image ):
	#
	#	converts to YCbCr Colorspace
	#
	image.convert("RGB") #image.convert("YCbCr") seems not to work, would be much easier
	pixels = image.load()

	for i in range(image.size[0]):
		for j in range (image.size[1]):
			r,g,b = pixels[i,j]			
			y = int(round(0 +0.299*r + 0.587*g + 0.114*b))
			cb = int(round(128 -0.168736*r -0.331364*g + 0.5*b))
			cr = int(round(128 +0.5*r - 0.418688*g - 0.081312*b))
			pixels[i,j] = (y, cb, cr)
	
	return image


def dctTransformation(image):

	def alpha( p , N):
			if p == 0:
				return math.sqrt(1/N)
			else:
				return math.sqrt(2/N)	

	def ac ( image, channel, u, v, N):
		sumresult = 0
		pixels = image.load()
		for x in range(N):
			for y in range(N):
				sumresult += pixels[x,y][channel] * math.cos((math.pi*(2*x+1)*u)/(2*N)) * math.cos((math.pi*(2*y+1)*v)/(2*N))
				#print(u,v,x,y)
		return alpha(u, N) * alpha(v, N) * sumresult

	'''
	N = 8
	yCoeffs = [[0 for x in range(N)] for y in range(N)] 
	cbCoeffs = [[0 for x in range(N)] for y in range(N)] 
	crCoeffs = [[0 for x in range(N)] for y in range(N)] 

	for u in range(N):
		for v in range(N):
			yCoeffs[u][v] = ac(image, 0, u, v, N)
			cbCoeffs[u][v] = ac(image, 1, u, v, N)
			crCoeffs[u][v] = ac(image, 2, u, v, N)

	#print(yCoeffs)
	#print(cbCoeffs)
	#print(crCoeffs)
	'''

	N = 8

	yDC = 0
	cbDC = 0
	crDC = 0
	yCoeffs = []
	cbCoeffs = []
	crCoeffs = []

	#Quantize DC: 6 Bit=64 , AC: 5 Bit=32

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
	'''
	start = timer()
	yDC, yCoeffs, cbDC, cbCoeffs, crDC, crCoeffs = dctTransformation(convertToYCbCr(shrinkImage(loadImage(filename))))
	end = timer()
	elapsed_time = end - start
	print("%.2fs :" % elapsed_time, filename)
	return yDC, yCoeffs, cbDC, cbCoeffs, crDC, crCoeffs
	'''

	return dctTransformation(convertToYCbCr(shrinkImage(loadImage(filename))))