import re
from timeit import default_timer as timer
from utilities import list_duplicates
from collections import defaultdict


index_dict = defaultdict(list)
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


def create_index(abstract, content_id):
    words = abstract.split()
    word_groups = list_duplicates(words)
    for group in word_groups:
        word = group[0]
        positions = group[1]
        word_index = (content_id, positions)
        index_dict[word].append(word_index)


def parse_file():
    file_input = open('long_abstracts_de.ttl', 'r', encoding='utf-8', errors='ignore')
    lines = file_input.readlines()
    count = len(lines)
    print("Parsing file...")

    for i in range(0, count):
        print_progress(i, count)

        line = lines[i].lower()
        if (line[0] != "#"):
            content_id, abstract = parse_line(line)
            create_index(abstract, content_id)

    print("Finished parsing file")
    file_input.close()
    return count


def write_index():
    file_output = open('outputfile.txt', 'w', encoding='utf-8', errors='ignore')
    delimiter = ": "
    count = len(index_dict)
    i = 0
    print("Writing index to file...")

    # Sort dictionary by the count of abstract ids in a descending order.
    # This is gonna take some time...
    for word in sorted(index_dict, key=lambda word: len(index_dict[word]), reverse=True):
        print_progress(i, count)

        ids = index_dict[word]
        file_output.write(word + delimiter + ", ".join(map(str, ids)) + "\n")
        i += 1

    print("Finished writing index to file")
    file_output.close()


def main():
    start = timer()
    line_count = parse_file()
    write_index()
    end = timer()
    elapsed_time = end - start
    print("Time to index %i abstracts: %.2f s" % (line_count, elapsed_time))


if __name__ == "__main__": main()
