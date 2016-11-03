
file_input = open('long_abstracts_de.ttl', 'r')
file_output = open('outputfile.txt', 'w')

x = file_input.readlines()
numId = 0

deleteChars = [')','(','[',']','"', '“', '„', '\\','=', '...', '↑']
replaceChars = ['.',',', ':', ';', '!', '?', '-', '–', '/']


def getContentId(text):
	numberOfSlash = 0
	contentId = ""
	for i in range (0,len(text)):
		if (text[i] == "/"):
			numberOfSlash += 1
		elif (text[i] == ">"):
			return contentId
		elif (numberOfSlash == 4):
			contentId += text[i]

def getAbstract(text):
	foundAbstract = False
	abstract = ""
	for i in range (0,len(text)):
		#if (foundAbstract and text[i] == '.' and text[i+1] =='"' and text[i+2] =='@' and text[i+3] =='d'):
		if (foundAbstract and text[i] == '@' and text[i+1] =='d' and text[i+2] =='e'):
			return abstract[0:len(abstract)-1]
		elif (foundAbstract):
			temp = text[i]
			for j in range (0,len(deleteChars)):
				temp = temp.replace(deleteChars[j], "")
			for k in range (0,len(replaceChars)):
				temp = temp.replace(replaceChars[k], " ")
			abstract += temp
		elif (text[i] == '"' and text[i-1] == ' ' and text[i-2] == '>'):
			foundAbstract = True

def createIndex(abstract, id):
	begin = 0
	end = 0
	i = 0
	while i < len(abstract):
		if abstract[i] == ' ':
			end = i
			if (len(abstract[begin:end].replace(" ","")) > 0): 
				with open ("index/"+abstract[begin:end],'a') as writeFile:
					with open ("index/"+abstract[begin:end],'r') as readFile:
						if (str(id) not in readFile.read()):
							with open("index/"+abstract[begin:end],'a') as writeFile:
								writeFile.write(id+"\n")
			begin = end+1
		i += 1


for i in range(0, len(x)):
	content = x[i].lower()
	contentId = ""
	if (content[0] != "#"):
		contentId = getContentId(content)
		if (i%1000 == 0):
			print(str(i)+"-"+contentId)
		abstract = getAbstract(content)
		createIndex(abstract, contentId)