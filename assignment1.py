# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 1
# Due Date: Jan 24th, 2022
# Description: Python Fundamentals Review

import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------


def min_max(arr: StaticArray) -> tuple:
    """
    TODO: Return the min and max values as a tuple without changing the static array.
    """
    length = arr.length()
    min_value = arr.get(0)
    max_value = arr.get(0)
    # find the values by linear search
    for i in range(length):
        min_value = arr.get(i) if arr.get(i) < min_value else min_value
        max_value = arr.get(i) if arr.get(i) > max_value else max_value
    # write the answer as a tuple
    ans = (min_value, max_value)
    return ans


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------


def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    TODO: Play fizz buzz game for the array without changing it.
    """
    length = arr.length()
    ansArr = StaticArray(length)
    # change the elements linearly and save them to the answer array
    for i in range(length):
        if arr.get(i) % 15 == 0:
            ansArr.set(i, 'fizzbuzz')
        elif arr.get(i) % 3 == 0:
            ansArr.set(i, 'fizz')
        elif arr.get(i) % 5 == 0:
            ansArr.set(i, 'buzz')
        else:
            ansArr.set(i, arr.get(i))
    return ansArr


# ------------------- PROBLEM 3 - REVERSE -----------------------------------


def reverse(arr: StaticArray) -> None:
    """
    TODO: Reverse the arr with O(n) complexity without creating another static array.
    """
    length = arr.length()
    mid = length // 2
    # switch the first and the last for n//2 times
    for i in range(mid):
        left = arr.get(i)
        right = arr.get(length - i - 1)
        arr.set(i, right)
        arr.set(length - i - 1, left)
    pass


# ------------------- PROBLEM 4 - ROTATE ------------------------------------


def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    TODO: With O(n) complexity, rotate the array to left or right steps times without changing the original array.
    """
    length = arr.length()
    ansArr = StaticArray(length)
    # calculate the remainder
    steps %= length
    # rotate right steps times with O(n) complexity
    for i in range(length):
        ansArr.set((i + steps) % length, arr.get(i))
    return ansArr


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------


def sa_range(start: int, end: int) -> StaticArray:
    """
    TODO: Build a static array contains consecutive integers from start to end.
    """
    # if we are creating an ascending array
    if start <= end:
        length = end - start + 1
        ans = StaticArray(length)
        # create a new static array with O(n) complexity
        for i in range(length):
            ans.set(i, start + i)
    # if we are creating an descending array
    else:
        length = start - end + 1
        ans = StaticArray(length)
        for i in range(length):
            ans.set(i, start - i)
    return ans


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------


def is_sorted(arr: StaticArray) -> int:
    """
    TODO: Determine if an array is ascending, descending, or neither.
    """
    length = arr.length()
    # only one element, return 0
    if length == 1:
        return 1
    first = arr.get(0)
    second = arr.get(1)
    # first two elements are ascending
    if first < second:
        # if part of the rest are descending, return 0
        for i in range(length - 1):
            if arr.get(i) >= arr.get(i + 1):
                return 0
        # if the array is ascending, return 1
        return 1
    # first two elements are descending
    elif first > second:
        # if part of the rest are ascending, return 0
        for i in range(length - 1):
            if arr.get(i) <= arr.get(i + 1):
                return 0
        # if the array is descending, return -1
        return -1
    # first two elements are the same, return 0
    else: return 0


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------


def find_mode(arr: StaticArray) -> tuple:
    """
    TODO: Find the mode element and its frequency with O(n) complexity
    """
    # the array is either non-descending or non-ascending
    length = arr.length()
    # set the first element as current value
    currentValue = arr.get(0)
    currentFrequency = 1
    mode = currentValue
    frequency = 1
    for i in range(1, length):
        # if there are more than one current value, add 1 to current value's frequency
        if arr.get(i) == currentValue:
            currentFrequency += 1
        else:
            # check if the current value is the new mode. if so, change the record
            if currentFrequency > frequency:
                mode, frequency = currentValue, currentFrequency
            # no matter the current value is the new mode or not, the current value changed
            currentValue = arr.get(i)
            currentFrequency = 1
    # if the last element if the mode, will need to check once again
    if currentFrequency > frequency:
        mode, frequency = currentValue, currentFrequency
    ans = (mode, frequency)
    return ans


# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------


def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    TODO: Create a new static array to remove the duplicates with O(n) complexity
    """
    length = arr.length()
    # find how many of duplicates elements do we have in total
    element = arr.get(0)
    count = 0
    for i in range(1, length):
        if arr.get(i) == element:
            count += 1
        else:
            element = arr.get(i)
    # create the answer array with a length of arr's length - duplicates count
    ansArr = StaticArray(length - count)
    # set the first element the same
    ansArr.set(0, arr.get(0))
    index = 0
    # from the second element, check duplicate
    for i in range(1, length):
        # if not duplicate, add this value and increment the index
        if arr.get(i) != ansArr.get(index):
            index += 1
            ansArr.set(index, arr.get(i))
    return ansArr


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------


def count_sort(arr: StaticArray) -> StaticArray:
    """
    TODO: Count sort an array in non-ascending order with O(n+k) complexity without changing the original array.
    """
    length = arr.length()
    ansArr = StaticArray(length)
    # find the max and min in the array using the min_max function
    (minValue, maxValue) = min_max(arr)
    # create a count array such that the first element represents the max value
    # the last element represents the min value, and the related data is the count
    # the length is max - min + 1, the additional space is for the rotation
    countLength = maxValue - minValue + 1 + 1
    countArr = StaticArray(countLength)
    # set every count number to 0
    for k in range(countLength):
        countArr.set(k, 0)
    # start counting
    for i in range(length):
        countArr.set(maxValue - arr.get(i), countArr.get(maxValue - arr.get(i)) + 1)
    # add up the count to get an ascending index array
    count = 0
    for k in range(countLength):
        count += countArr.get(k)
        countArr.set(k, count)
    # rotate the countArray to right once and change the first data to 0
    countArr = rotate(countArr, 1)
    countArr.set(0, 0)
    # print the ansArray, the time complexity here is actually O(n)
    for k in range(countLength - 1):
        for i in range(countArr.get(k), countArr.get(k + 1)):
            ansArr.set(i, maxValue - k)
    return ansArr


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------


def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    TODO: Create an array to save squared values of the array in non-descending order.
    This is a tricky question. Fortunately, it is sorted.
    My idea is to start with the first and last elements, find the bigger abs one
    Then add that square to my answer arr.
    """
    length = arr.length()
    ansArray = StaticArray(length)
    left, right = 0, length - 1
    index = length - 1
    while index >= 0:
        if abs(arr.get(left)) <= abs(arr.get(right)):
            ansArray.set(index, arr.get(right) ** 2)
            right -= 1
        else:
            ansArray.set(index, arr.get(left) ** 2)
            left += 1
        index -= 1
    return ansArray


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(min_max(arr))

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(min_max(arr))

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(min_max(arr))

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        print(rotate(arr, steps), steps)
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-105, -99), (-99, -105)]
    for start, end in cases:
        print(start, end, sa_range(start, end))

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print('Result:', is_sorted(arr), arr)

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        mode, frequency = find_mode(arr)
        print(f"{arr}\nMode: {mode}, Frequency: {frequency}\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr if len(case) < 50 else 'Started sorting large array')
        result = count_sort(arr)
        print(result if len(case) < 50 else 'Finished sorting large array')

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')
