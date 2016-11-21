import re
from timeit import default_timer as timer
from utilities import list_duplicates, open_file, characters, character_group_count, characters_group
from collections import defaultdict


word_dict = defaultdict(list)
symbol_dict = defaultdict(list)
deleteChars = [')','(','[',']','"', '“', '„', '\\','=', '...', '↑']
replaceChars = ['.',',', ':', ';', '!', '?', '-', '–', '/']


def print_progress(current, total):
    if (current % 10000 == 0 or current == total - 1):
        percent = min(current / total * 100, 100)
        print("Progress: %.2f%%" % percent)


def parse_line(text):
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
    words = abstract.split()
    word_groups = list_duplicates(words)
    for group in word_groups:
        word = group[0]
        positions = group[1]
        word_index = (content_id, positions)

        initial_char = word[0]
        if initial_char in character_group:
            word_dict[word].append(word_index)

        if group_index == 0 and initial_char not in characters:
            symbol_dict[word].append(word_index)


def parse_file(group_index):
    file_input = open('long_abstracts_de.ttl', 'r', encoding='utf-8', errors='ignore')
    lines = file_input.readlines()
    count = len(lines)
    print("Parsing file for index %i..." % group_index)

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

    print("Finished parsing file")
    file_input.close()
    return result


def write_word_index(group_index):
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
    start = timer()

    abstract_ids = []
    group_count = character_group_count()

    for group_index in range(0, group_count):
        abstract_ids = parse_file(group_index)

        if group_index == 0:
            write_symbol_index()
            write_abstract_ids(abstract_ids)

        write_word_index(group_index)

    end = timer()
    elapsed_time = end - start
    abstract_count = len(abstract_ids)
    print("Time to index %i abstracts: %.2f s" % (abstract_count, elapsed_time))


if __name__ == "__main__": main()
