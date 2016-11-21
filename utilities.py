from itertools import groupby
from collections import defaultdict


characters = ["a", "ä", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "ö", "p", "q", "r", "s", "t", "u", "ü", "v", "w", "x", "y", "z"]
characters_group_size = 5


def characters_group(group_index):
    start_index = characters_group_size * group_index
    end_index = start_index + characters_group_size if len(characters) > start_index + characters_group_size else len(characters)
    return characters[start_index:end_index]


def character_group_count():
    group_count = int(len(characters) / characters_group_size)
    group_count += 0 if len(characters) % characters_group_size == 0 else 1

    return group_count


def group_for_character(char):
    group_count = character_group_count()

    for index in range(0, group_count):
        if char in characters_group(index):
            return index

    return None


def file_name_for_char(char):
    group_index = group_for_character(char)

    if group_index is not None:
        return "index/index" + str(group_index) + ".txt"
    else:
        return "index/other.txt"


def open_file(file_name, mode="r"):
    return open(file_name, mode, encoding='utf-8', errors='ignore')


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


def group_words_with_positions(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key, locs in tally.items() if len(locs) > 0)


def common_elements(list1, list2):
    temp_list1 = list(map(lambda x: x[0], list1))
    temp_list2 = list(map(lambda x: x[0], list2))

    result = []
    for i, element in enumerate(temp_list1):
        j = temp_list2.index(element) if element in temp_list2 else -1
        if j >= 0:
            positions = list1[i][1] + list2[j][1]
            temp_list2.pop(j)

            result.append((element, positions))
        else:
            position = list1[i][1]
            result.append((element, position))

    return result


def unique_elements(list1, list2):
    temp_list1 = list(map(lambda x: x[0], list1))
    temp_list2 = list(map(lambda x: x[0], list2))

    result = []
    for i, element in enumerate(temp_list1):
        j = temp_list2.index(element) if element in temp_list2 else -1
        if j >= 0:
            positions = list1[i][1] + list2[j][1]
            temp_list2.pop(j)

            result.append((element, positions))
        else:
            position = list1[i][1]
            result.append((element, position))

    for i, element in enumerate(temp_list2):
        position = list2[i][1]
        result.append((element, position))

    return result


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
