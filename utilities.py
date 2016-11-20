from itertools import groupby
from collections import defaultdict


def group_search_results(results, length):
    result_dict = defaultdict(list)
    sorted_results = sorted(results)

    for content_id, group in groupby(sorted_results, lambda x: x[0]):
        word_positions = []
        group_size = 0

        for value in group:
            word_positions.append((value[1], value[2]))
            group_size += 1

        if group_size == length:
            result_dict[content_id] = word_positions

    return result_dict


def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key, locs in tally.items() if len(locs) > 0)


def unique_elements(list1, list2):
    result = set(list1 + list2)
    return list(result)


def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)


def is_int(value):
    try:
        int(value)
        return True
    except:
        return False
