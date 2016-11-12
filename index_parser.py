import re
from timeit import default_timer as timer
from collections import defaultdict

index_dict = defaultdict(set)

file_input = open('long_abstracts_de.ttl', 'r')
file_output = open('outputfile.txt', 'w')

x = file_input.readlines()

deleteChars = [')','(','[',']','"', '“', '„', '\\','=', '...', '↑']
replaceChars = ['.',',', ':', ';', '!', '?', '-', '–', '/']

def parseLine(text):
	result = re.search('resource\/(.*)>\s<[a-zA-Z:\/\.]*>\s"(.*)"@de', text)
	if result:
		content_id = result.group(1)
		abstract = result.group(2)
		for char in deleteChars:
			abstract = abstract.replace(char, "")
		for char in replaceChars:
			abstract = abstract.replace(char, " ")
		return content_id, abstract

def createIndex(abstract, id):
	words = abstract.split()
	for index, word in enumerate(words):
		id_index = (id, index)
		index_dict[word].add(id_index)

start = timer()
for i in range(0, len(x)):
    content = x[i].lower()
    if (content[0] != "#"):
        content_id, abstract = parseLine(content)
        createIndex(abstract, content_id)
        if (i % 1000 == 0):
            print(str(i) + "-" + content_id)

for word, ids in index_dict.items():
    delimiter = ": "
    file_output.write(word + delimiter + ", ".join(map(str, ids)) + "\n")

file_output.close()

end = timer()
elapsed_time = end - start

print("Time to index %i abstracts: %.2f" % (len(x), elapsed_time))
