import sys
import os
from timeit import default_timer as timer
from analyze import createDescriptor

from xml.dom.minidom import parse
import xml.dom.minidom

entireGroup, branchGroup, flowerGroup, fruitGroup, leafGroup, leafScanGroup, stemGroup, miscGroup = [], [], [], [], [], [], [], []

def getContentType (filename):
	#	get the content type of an file.xml
	#	e.g. Leaf or Flower
	#
	DOMTree = xml.dom.minidom.parse(filename)
	image = DOMTree.documentElement
	try:
		content = image.getElementsByTagName("Content")[0].childNodes[0].data
	except: # if no group specified or typo
		content = "NoContentType"
	return content


def getGroup( str ):
	#
	#	returns the corresponding group, in which the element belongs
	#
	if str == "Entire":
		return entireGroup
	elif str == "Branch":
		return branchGroup
	elif str == "Flower":
		return flowerGroup
	elif str == "Fruit":
		return fruitGroup
	elif str == "Leaf":
		return leafGroup
	elif str == "LeafScan":
		return leafScanGroup
	elif str == "Stem":
		return stemGroup
	else: # if no group specified or typo
		return miscGroup


def writeIndex(filename):
	#
	#	Write the index to file
	#	csv -> Content, yDC, yCoeffs, cbDC, cbCoeffs, crDC, crCoeffs, MediaId
	#
	fileoutput = open(filename, "w+", encoding='utf-8', errors='ignore')
	for item in entireGroup:
		fileoutput.write("Entire," + item + "\n") 
	for item in branchGroup:
		fileoutput.write("Branch," + item + "\n") 
	for item in flowerGroup:
		fileoutput.write("Flower," + item + "\n") 
	for item in fruitGroup:
		fileoutput.write("Fruit," + item + "\n") 
	for item in leafGroup:
		fileoutput.write("Leaf," + item + "\n") 
	for item in leafScanGroup:
		fileoutput.write("LeafScan," + item + "\n") 
	for item in stemGroup:
		fileoutput.write("Stem," + item + "\n") 
	for item in miscGroup:
		fileoutput.write("null," + item + "\n") 


def main():
	#
	#	main
	#
	print("Color Layout Description Index Builder")
	print("--------------------------------------")
	start = timer()
	directory = "PlantCLEF2016Test"
	indexFilename = "index.csv"
	listdir = os.listdir(directory)
	filecount = 0
	progress = 0
	s = " "; # seperator for the coefficients

	# counting all files in the directory, excluding hidden dot-files
	for filename in listdir:
		if filename.endswith(".jpg") and filename[0] != '.':
			filecount += 1

	# going through all jpg files and calculating the descriptor
	# get the contentype via the xml file
	for filename in listdir:		
		if filename.endswith(".jpg") and filename[0] != '.':
			path = os.path.join(directory, filename)			

			# calculate descriptor
			yDC, yCoeffs, cbDC, cbCoeffs, crDC, crCoeffs = createDescriptor(path)

			# get the content type
			contentType = getContentType(path.replace("jpg", "xml"))
			
			# write entry in corresponding content-group list
			getGroup(contentType).append(str(yDC) +','+ s.join(str(x) for x in yCoeffs) +','+ str(cbDC) +','+ s.join(str(x) for x in cbCoeffs) +','+ str(crDC) +','+ s.join(str(x) for x in crCoeffs) +','+ filename.replace(".jpg", ""))

			progress += 1			
			print ("Building index..%.2f%%" % (progress/filecount*100), end="\r")
			
			if progress == 100: # DEBUG for not building the whole index
				break
				
	print("B") # some litte workaround to start a new line
	print("Write index to file..")

	# write all entrys to file
	writeIndex(indexFilename)

	end = timer()
	elapsed_time = end - start

	print("Done in %.2fs" % elapsed_time)


if __name__ == "__main__": main() 