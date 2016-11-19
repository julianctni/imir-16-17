import re
from index_parser import parse_line
from tree import *


abstract_file, abstract_lines, abstract_count = (None, None, None)
index_file, index_lines, index_count = (None, None, None)
search_blocks = []


def is_int(value):
    try:
        int(value)
        return True
    except:
        return False


def search(term):
    print("Searching for %s" % term)

    result = []
    for i in range(0, index_count):
        index_line = index_lines[i]
        content = index_line.split(": ")
        word = content[0]
        if word == term:
            abstracts = [int(n) for n in content[1].split(", ")]
            for abstract in abstracts:
                line_number = abstract
                result.append(line_number)
            break
    if len(result) == 0:
        print("Could not find any abstracts with the provided search term '%s'." % term)

    print("Total resources: %i" % len(result))
    print("------------------")

    return result


def prepare_query(query):
    global search_blocks

    results = re.findall("(\([^\(\)]*\))", query)
    if len(results) == 0:
        if len(search_blocks) == 0:
            search_blocks = [query]
        return search_blocks

    search_term = query
    for result in results:
        index = str(len(search_blocks))
        search_term = search_term.replace(result, index)
        search_blocks.append(result)

    return prepare_query(search_term)


def build_tree(search_block):
    tree = BinaryTree(None)
    result = re.search("\((?:|([^()]*)\s)(AND|OR|NOT)\s([^()]*)", search_block, re.IGNORECASE)

    if result:
        left = result.group(1)
        operator = result.group(2)
        right = result.group(3)

        if left is None:
            tree.set_node_value(NotOperatorNode(abstract_count))

            if is_int(right):
                right = int(right)
                tree.left = build_tree(search_blocks[right])
                tree.left.parent = tree
            else:
                left_node = TermNode(right, search)
                tree.insert_left(left_node)
        else:
            if operator == "and":
                tree.set_node_value(AndOperatorNode())
            elif operator == "or":
                tree.set_node_value(OrOperatorNode())

            if is_int(left):
                left = int(left)
                tree.left = build_tree(search_blocks[left])
                tree.left.parent = tree
            else:
                left_node = TermNode(left, search)
                tree.insert_left(left_node)

            if is_int(right):
                right = int(right)
                tree.right = build_tree(search_blocks[right])
                tree.right.parent = tree
            else:
                right_node = TermNode(right, search)
                tree.insert_right(right_node)
    else:
        node = TermNode(search_block, search)
        tree.set_node_value(node)

    return tree


def print_results(results):
    print("Total results: %i" % len(results))
    print("Found in:")
    for result in results:
        abstract = abstract_lines[result]
        content_id, _ = parse_line(abstract)
        print(content_id)
    print("------------------")


def main():
    global abstract_file, abstract_lines, abstract_count
    global index_file, index_lines, index_count
    global search_blocks
    abstract_file = open('long_abstracts_de.ttl', 'r')
    abstract_lines = abstract_file.readlines()
    abstract_count = len(abstract_lines)
    index_file = open('outputfile.txt', 'r')
    index_lines = index_file.readlines()
    index_count = len(index_lines)

    while True:
        # Sample query: ((bonobo AND sprache) AND (NOT völkermord))
        raw_query = input("Enter search query: ").lower()
        prepare_query(raw_query)
        query_tree = build_tree(search_blocks[-1])
        results = query_tree.evaluate()
        print_results(results)
        search_blocks = []

    abstract_file.close()
    index_file.close()

if __name__ == "__main__": main()
