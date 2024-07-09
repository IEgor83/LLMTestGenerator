import random


def _shuffle_list(array):
    """
    shuffle list and all lists in him
    """
    try:
        random.shuffle(array)
    # if array not a list
    except TypeError:
        return
    # else continue shuffle lists
    for sub_list in array:
        _shuffle_list(sub_list)


def shuffle_list(array):
    """
    create a new list, shuffle him and return
    """
    _array = list(array)
    _shuffle_list(_array)
    return _array
