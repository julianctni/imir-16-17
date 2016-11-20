def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


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
