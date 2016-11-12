import re
from index_parser import parse_line
from ast import literal_eval as make_tuple

def search(term):
    abstract_file = open('long_abstracts_de.ttl', 'r')
    abstract_lines = abstract_file.readlines()
    abstract_count = len(abstract_lines)
    index_file = open('outputfile.txt', 'r')
    index_lines = index_file.readlines()
    index_count = len(index_lines)

    result = []
    for i in range(0, index_count):
        index_line = index_lines[i]
        content = index_line.split(": ")
        word = content[0]
        if word == term:
            abstracts = make_tuple("[" + content[1] + "]")
            print("Found search term '%s' in the following abstracts:" % term)
            for abstract in abstracts:
                line_number = abstract[0]
                line = abstract_lines[line_number]
                content_id, _ = parse_line(line)
                position = abstract[1]
                print("%s at position %i" % (content_id, position))
                result.append((content_id, position))
            continue
        if i == index_count - 1 and len(result) == 0:
            print("Could not find any abstracts with the provided search term '%s'." % term)

    abstract_file.close()
    index_file.close()
    return result

def prepare_search(query):
    pattern = re.compile(r'(AND|OR|NOT)')
    operators = []
    for operator in re.findall(pattern, query):
        operators.append(operator)
    re.sub(pattern, " ", query).split()

def main():
    while True:
        search_term = input("Enter search term: ").lower()
        result = search(search_term)
        print("------------------")
        print("Total resources: %i" % len(result))
        print("------------------")

if __name__ == "__main__": main()

#cut search term in multiple search terms later (AND, OR, etc)

#loop through all indexed files with the specified name/attribute

