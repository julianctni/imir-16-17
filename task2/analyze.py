import sys
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

	print(path, "(", image.width, "x", image.height, ") loaded")
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


def main():
	#
	#	main function
	#
	start = timer()

	print("Loading image..")
	image = loadImage(sys.argv[-1])
	image.resize((256,256),Image.NEAREST).show(); #deeeebug!!

	print("Representative color selection...")
	image = shrinkImage(image)	
	image.resize((256,256),Image.NEAREST).show(); #deeeebug!!

	print("Convert image to YCbCr..")
	image = convertToYCbCr(image)
	image.resize((256,256),Image.NEAREST).show(); #deeeebug!!

	end = timer()
	elapsed_time = end - start

	print("Done in %.2fs" % elapsed_time)


if __name__ == "__main__": main()