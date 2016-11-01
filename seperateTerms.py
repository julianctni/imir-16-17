file_input = open('long_abstracts_de.ttl', 'r')
file_output = open('outputfile.txt', 'w')

x = file_input.read()


def getWords():
	i = 0
	hasBegin = False
	begin = 0
	end = 0
	jump = False
	while i < 500:
		if x[i] == ' ':
			if hasBegin == True:
				end = i
				if x[i-1] == ',' or x[i-1] == '.' or x[i-1] == '(' or x[i-1] == ')' or x[i-1] == '"' or x[i-1] == '-' or x[i-1] == ';':
					print(x[begin:end-1])
				else:
					print(x[begin:end])

				if x[i+1] == ',' or x[i+1] == '.' or x[i+1] == '(' or x[i+1] == ')' or x[i+1]== '"' or x[i+1] == '-' or x[i+1] == ';':					
					begin = end+2
				else:
					begin = end+1
			else:
				begin = i+1
				hasBegin = True
		i += 1

getWords()