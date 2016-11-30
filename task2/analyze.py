import sys
from PIL import Image

#	analyze.py
#
#	use: python3 analyze.py example.jpg
#


def loadImage( path ):
	image = Image.open(path)
	print(path, ",", image.width, "x", image.height)
	return image


def convertToYCbCr( image ):
	image.convert("RGB") #image.convert("YCbCr") seems not to work, would be much easier
	newImage = Image.new("YCbCr", image.size) #switch with "RGB" to see that the conversion works
	newPixels = newImage.load()

	for i in range(image.size[0]):
		for j in range (image.size[1]):
			r,g,b = image.getpixel((i,j))
			
			y = int(round(0 +0.299*r + 0.587*g + 0.114*b))
			cb = int(round(128 -0.168736*r -0.331364*g + 0.5*b))
			cr = int(round(128 +0.5*r - 0.418688*g - 0.081312*b))

			newPixels[i,j] = (y, cb, cr)
	
	return newImage


def analyzeImage( image ):
	for i in range(image.size[0]):
		for j in range (image.size[1]):
			r,g,b = image.getpixel((i,j))
			#print(r,g,b)

	#Cosine Transformation, etc.


def main():
	print("loading image..")
	image = loadImage(sys.argv[-1])
	print("convert image..")
	image = convertToYCbCr(image)
	print("done")
	analyzeImage(image)
	image.show()


if __name__ == "__main__": main()