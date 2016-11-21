import re
from utilities import is_int, group_search_results, file_name_for_char, open_file
from collections import defaultdict
from tree import *


abstract_ids_file, abstract_ids_lines = (None, None)
search_blocks = []


def search(term):
    """
    Searches for a given term in the corresponding index file. The index file
    is determined by the initial character of the given term. After the file
    has been opened, each line is searched for the term. If it has been found,
    the abstract ids and the positions of the term in the abstracts are parsed
    and added to the result dictionary.

    Args:
        term: one word

    Returns:
        returns a dictionary of abstract ids that contain the given term
    """
    print("Searching for %s" % term)

    initial_char = term[0]
    file_name = file_name_for_char(initial_char)
    index_file = open_file(file_name)
    index_lines = index_file.readlines()
    index_count = len(index_lines)

    result = defaultdict(list)
    for i in range(0, index_count):
        index_line = index_lines[i]
        content = index_line.split(": ")
        word = content[0]
        if word == term:
            abstracts = re.findall("\(\'([^']*)\',\s\[([^)]*)\]\)", content[1])
            for abstract in abstracts:
                content_id = abstract[0]
                positions = list(map(int, abstract[1].split(", ")))
                result[content_id] = positions
            break
    if len(result) == 0:
        print("Could not find any abstracts with the provided search term '%s'." % term)

    print("Total resources: %i" % len(result))
    print("------------------")

    index_file.close()

    return result


def search_phrase(phrase):
    """
    Searches for the given phrase. In a first step, every word in the phrase will be
    searched separately. The search results from the individual search queries are
    added to a dictionary, which is flattened out to a list of search results that
    consist of the abstract id, the word and its positions in the abstract.
    After that list entries with the same abstract id are grouped together and stored
    alongside the words and their positions in the abstract.
    The entries in the dictionary are passed to the find_consecutive_positions-function,
    which examines if the words in the phrase appear consecutively. If this is the case,
    the id of the corresponding abstract and the word positions are added to the result
    set.

    Args:
        phrase: a group of words that appear in their described order

    Returns:
        returns a dictionary of abstract ids that contain the given phrase
    """
    results = defaultdict(list)
    search_results = defaultdict(list)
    words = phrase.split()

    # Search for every word in the phrase and store the search results
    for word in words:
        search_results[word] = search(word)

    print("Calculating search results for phrase \"%s\"" % phrase)

    search_list = []
    for word, result in search_results.items():
        for content_id, positions in result.items():
            search_list.append((content_id, word, positions))

    grouped_search_results = group_search_results(search_list, len(words))

    for content_id, value in grouped_search_results.items():
        found_at = find_consecutive_positions(value, words)

        if len(found_at) > 0:
            results[content_id] = found_at

    print("Finished calculating search results")

    return results


def find_consecutive_positions(tuple_list, words, position=None):
    """
    Determines recursively if a group of words appears consecutively in
    a given text. The text is represented by a list of tuples, that each contain
    a word and its position in the text.

    Args:
        tuple_list: a list of tuples, that each contain a word and its position in a text.
        words: a group of words, that shall appear consecutively.
        position: a number that represents the position where the next word is to be expected.

    Returns:
        returns a list of the positions, where the group of words have been found
    """
    # Stop the recursion and return true, if the words appear consecutively.
    if len(words) == 0:
        return position

    word = words[0]
    # Get all tuples that contain the first word
    tuples = [tuple for tuple in tuple_list if tuple[0] == word]

    # The position parameter is not set for the first call of the function
    if position is not None:
        # Get tuples that appear at the given position
        tuples = [tuple for tuple in tuples if position in tuple[1]]

    # Stop the recursion and return None, if the words do not appear consecutively.
    if len(tuples) == 0:
        return None

    found_at = []
    for tuple in tuples:
        positions = tuple[1]
        for index, position in enumerate(positions):
            # Call function recursively with an updated list of words, where the first
            # word is removed, and an incremented position.
            if find_consecutive_positions(tuple_list, words[1:], position + 1):
                found_at.append(position)

    return found_at


def prepare_query(query):
    """
    Creates a list of search blocks from a given query string. Each search block
    represents a single search query that is enclosed by parenthesis, but does not contain
    parenthesis:
        - (mensch AND auto) is a single search query
        - ((mensch OR tier) AND auto) is not. It is a nested search query.
    Search blocks from deeply nested search queries are retrieved recursively.
    The list of search blocks is constructed from the bottom-up. Queries which are deeper
    in the hierarchy are at the beginning of the list.

    Args:
        query: a query string with optional nesting

    Returns:
        returns a list of search blocks
    """
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


def return_search_function(term):
    """
    Determines the appropriate search function for a given term. If the term is
    enclosed by parenthesis, it is expected to be a phrase. Therefore the function,
    which is responsible for phrase search, is returned.

    Args:
        term: one word or a phrase, which is enclosed by parenthesis

    Returns:
        returns the appropriate search function for a given term
    """
    first = term[0]
    last = term[-1]

    if first == "\"" and last == "\"":
        return search_phrase
    else:
        return search


def build_tree(search_block):
    """
    Creates a binary tree from a search block. A search block can have the following structures:
        - (term1 AND term2), (term2 OR term2)
        - (NOT term1)
    Search terms and phrases are interchangeable.

    Args:
        search_block: a search block that can reference nested search blocks

    Returns:
        returns a binary tree that represents the initial search block and therefore the input query
    """
    tree = BinaryTree(None)
    result = re.search("\((?:|([^()]*)\s)(AND|OR|NOT)\s([^()]*)", search_block, re.IGNORECASE)

    if result:
        left = result.group(1)
        operator = result.group(2)
        right = result.group(3)

        if left is None:
            tree.set_node_value(NotOperatorNode(abstract_ids_lines))

            if is_int(right):
                right = int(right)
                tree.left = build_tree(search_blocks[right])
                tree.left.parent = tree
            else:
                term = right.strip("\"")
                left_node = TermNode(term, return_search_function(right))
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
                term = left.strip("\"")
                left_node = TermNode(term, return_search_function(left))
                tree.insert_left(left_node)

            if is_int(right):
                right = int(right)
                tree.right = build_tree(search_blocks[right])
                tree.right.parent = tree
            else:
                term = right.strip("\"")
                right_node = TermNode(term, return_search_function(right))
                tree.insert_right(right_node)
    else:
        term = search_block.strip("\"")
        node = TermNode(term, return_search_function(search_block))
        tree.set_node_value(node)

    return tree


def print_results(results):
    print("Found in:")
    for content_id, positions in results.items():
        print("%s (%i times)" % (content_id, len(positions)))
    print("------------------")
    print("Total results: %i" % len(results))
    print("------------------")


def main():
    global abstract_ids_file, abstract_ids_lines
    global search_blocks
    abstract_ids_file = open_file('index/abstractids.txt')
    abstract_ids_lines = abstract_ids_file.read().splitlines()

    while True:
        print("")
        print("Please take a look of the following query types you may use.")
        print("------------------------------------------------------------")
        print("Option A: Searching for a single term: obama")
        print('Option B: Searching for a phrase: "american president"')
        print('Option C: Combination of terms/phrases and Boolean operators [OR/AND/NOT]: (obama AND (NOT "american president"))')
        print("------------------------------------------------------------")
        raw_query = input("Enter search query: ").lower()
        prepare_query(raw_query)
        query_tree = build_tree(search_blocks[-1])
        results = query_tree.evaluate()
        print_results(results)
        search_blocks = []

    abstract_ids_file.close()

if __name__ == "__main__": main()
