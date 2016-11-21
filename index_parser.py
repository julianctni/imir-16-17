import re
from timeit import default_timer as timer
from utilities import group_words_with_positions, open_file, characters, character_group_count, characters_group
from collections import defaultdict


word_dict = defaultdict(list)
symbol_dict = defaultdict(list)
deleteChars = [')','(','[',']','"', '“', '„', '\\','=', '...', '↑']
replaceChars = ['.',',', ':', ';', '!', '?', '-', '–', '/']



def print_progress(current, total):
	"""
	Prints the progress of the current process (parsing/writing to file).

	Args:
		current: current progress value

		total: target/total progress value
	"""
	if (current % 10000 == 0 or current == total - 1):
		percent = min(current / total * 100, 100)
		print("Progress: %.2f%%" % percent, end="\r")


def parse_line(text):
	"""
	Parses one line of the input file and extracts the id of the abstract and
	removes or replaces some predefined (see arrays deleteChars andreplaceChars)
	chars from the abstract text, which are not needed for indexing.

	Args:
		text: the text of one line 

	Returns:
		returns the id of the current abstract and the abstract text without any punctuation marks or brackets.
	"""
	result = re.search('resource\/(.*)>\s<[a-zA-Z:\/\.]*>\s"(.*)"@de', text)
	if result:
		content_id = result.group(1)
		abstract = result.group(2)
		for char in deleteChars:
			abstract = abstract.replace(char, "")
		for char in replaceChars:
			abstract = abstract.replace(char, " ")
		return content_id, abstract


def create_index(abstract, content_id, character_group, group_index):
	"""
	Creates all index data for an abstract.
		1. split text into single terms.
		2. make tuples of terms and an array containing their positions in the text, e.g. ('car', [0,4,6])
		3. check the first char of each term, whether it belongs to the current character_group or is a special char/number
			case 1: char belongs to current character group
			case 2: char does not belong to current character_group, but is a special char/number
			case 3: char does not belong to current character_group and is not a special char/number
		4. if case 1 or 3 -> add tuple to the corresponding dictionariy (word_dict or symbol_dict)

	Args:
		abstract: preprocessed abstract text (see function parse_line)

		content_id: id of the abstract containing the term

		character_group: character group of the first char of the term (aäbcd, efghi, jklmn, oöpq, stuüv, wxyz, special chars/numbers)

		group_index: index of the current character group
	"""
	words = abstract.split()
	word_groups = group_words_with_positions(words)
	for group in word_groups:
		word = group[0]
		positions = group[1]
		word_index = (content_id, positions)

		initial_char = word[0]
		if initial_char in character_group:
			word_dict[word].append(word_index)

		elif group_index == 0 and initial_char not in characters:
			symbol_dict[word].append(word_index)


def parse_file(group_index, group_count, character_group):
	"""
	Opens the abstracts file and reads it line after line. Calls the parse_line() to 
	receive abstract id and preprocessed abstract text. After that it calls create_index()
	to add the index data to the dict variables for each line/abstract and character group.

	Args:
		group_index: index of the current character group

	Returns:
		returns an array containing all abstract ids (only needed during first indexing iteration)
	"""
	file_input = open('long_abstracts_de.ttl', 'r', encoding='utf-8', errors='ignore')
	lines = file_input.readlines()
	count = len(lines)
	print("Parsing file for index %i (%s) of %i..." % (group_index, ', '.join(character_group), group_count-1))

	group = characters_group(group_index)

	result = []
	for i in range(0, count):
		print_progress(i, count)

		line = lines[i].lower()
		if (line[0] == "#"):
			continue

		content_id, abstract = parse_line(line)
		create_index(abstract, content_id, group, group_index)
		result.append(content_id)

	print("Finished parsing file for character group %s" %', '.join(character_group))
	file_input.close()
	return result


def write_word_index(group_index):
	"""
	Writes the content of the word dictionary (word_dict) to the index file of the character group.
	The formatting of the index file looks like this:

	term: (abstract id, [positions])

	Args:
		group_index: index of the current character group
	"""
	file_output = open_file("index/index" + str(group_index) + ".txt", "w")

	delimiter = ": "
	count = len(word_dict)
	i = 0
	print("Writing word index %i to file..." % group_index)

	# Sort dictionary by the count of abstract ids in a descending order.
	# This is gonna take some time...
	for word in sorted(word_dict, key=lambda word: len(word_dict[word]), reverse=True):
		print_progress(i, count)

		ids = word_dict[word]
		file_output.write(word + delimiter + ", ".join(map(str, ids)) + "\n")

		i += 1

	print("Finished writing word index to file")

	word_dict.clear()
	file_output.close()


def write_symbol_index():
	"""
	Writes the content of the dictionary containing terms which start with a
	special chars or a number numbers (symbol_dict) to the corresponding index file.
	This function is only called once, because all all numbers/special chars are
	found in the first iteration of indexing.

	The formatting of the index file looks like this:
	
	term: (abstract id, [positions])
	"""
	file_output = open_file("index/other.txt", "w")

	delimiter = ": "
	count = len(symbol_dict)
	i = 0
	print("Writing symbol index to file...")

	for symbol in symbol_dict:
		print_progress(i, count)

		ids = symbol_dict[symbol]
		file_output.write(symbol + delimiter + ", ".join(map(str, ids)) + "\n")

		i += 1

	print("Finished writing symbol index to file")

	symbol_dict.clear()
	file_output.close()



def write_abstract_ids(abstract_ids):
	"""
	Writes all abstract ids to an extra file. This file is important for boolean NOT search.

	The formatting of the index file looks like this:
	
	abstract id 1
	abstract id 2
	abstract id 3
	...

	The function is only called once after the first iteration of indexing.

	Args:
		abstract_ids: an array containing all abstract ids
	"""
	file_output = open_file("index/abstractids.txt", "w")
	count = len(abstract_ids)

	print("Writing abstract ids to file...")

	for index, abstract_id in enumerate(abstract_ids):
		print_progress(index, count)

		delimiter = "\n" if index < count else ""
		file_output.write(abstract_id + delimiter)

	print("Finished abstract ids to file")

	file_output.close()



def main():
	"""
	Main function which starts the indexing process.
	First it calculates the size of the number of character groups (see utilites.py).
	The default value (characters_group_size in utilities.py) is set to 5, which works with a RAM size of 8GB.
	On systems with a smaller RAM size, it should be set to a lower value (see utilites.py).

	After that it starts the indexing for each character group. With the default value of 5 there are
	six iterations and the following character groups: aäbcd, efghi, jklmn, oöpq, stuüv, wxyz, special chars / numbers.
	During the first iteration (default: aäbcd) it furthermore writes the index for special chars / numbers and the 
	file containing all abstract ids.
	"""
	start = timer()

	abstract_ids = []
	group_count = character_group_count()

	for group_index in range(0, group_count):
		abstract_ids = parse_file(group_index, group_count, characters_group(group_index))

		if group_index == 0:
			write_symbol_index()
			write_abstract_ids(abstract_ids)

		write_word_index(group_index)

	end = timer()
	elapsed_time = end - start
	abstract_count = len(abstract_ids)
	print("Time to index %i abstracts: %.2f s" % (abstract_count, elapsed_time))


if __name__ == "__main__": main()
