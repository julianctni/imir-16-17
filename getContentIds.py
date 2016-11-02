file_input = open('long_abstracts_de.ttl', 'r')
file_output = open('outputfile.txt', 'w')

x = file_input.readlines()
numId = 0


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
		if (foundAbstract and text[i] == '"' and text[i+1] =='@' and text[i+2] =='d' and text[i+3] =='e'):
			return abstract
		elif (foundAbstract):
			abstract += text[i]
		elif (text[i] == '"' and text[i-1] == ' ' and text[i-2] == '>'):
			foundAbstract = True

	
for i in range(1, 10):
	content = x[i].lower()
	contentId = ""
	if (content[0] != "#"):
		contentId = getContentId(content)
		print(str(i)+"-"+contentId)
		abstract = getAbstract(content)
		hasBegin = False
		begin = 0
		end = 0
		while i < len(abstract):
			if abstract[i] == ' ':
				if hasBegin == True:
					end = i
					if abstract[i-1] == ',' or abstract[i-1] == '.' or abstract[i-1] == '(' or abstract[i-1] == ')' or abstract[i-1] == '"' or abstract[i-1] == '-' or abstract[i-1] == ';':
						print(abstract[begin:end-1])
					else:
						print(abstract[begin:end])

					if abstract[i+1] == ',' or abstract[i+1] == '.' or abstract[i+1] == '(' or abstract[i+1] == ')' or abstract[i+1]== '"' or abstract[i+1] == '-' or abstract[i+1] == ';':					
						begin = end+2
					else:
						begin = end+1
				else:
					begin = i+1
					hasBegin = True
			i += 1
		#print (getAbstract(content))
		print("")