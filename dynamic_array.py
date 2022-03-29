# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: Jan 31, 2022
# Description: Part 1 - Implement the Dynamic Array Class

from static_array import *


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.size = 0
        self.capacity = 4
        self.data = StaticArray(self.capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self.size) + "/" + str(self.capacity) + ' ['
        out += ', '.join([str(self.data[_]) for _ in range(self.size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self.index]
        except StaticArrayException:
            raise StopIteration
        self.index = self.index + 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        return self.data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        self.data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        This method is intended to be an "internal" method to change the capacity
        of the underlying storage for the array elements.
        """
        if new_capacity <= 0 or new_capacity < self.size or new_capacity == self.capacity:
            # when new capacity is not positive, or smaller than element size, or equal to current capacity
            return
        # create a new static array with new capacity
        new_data = StaticArray(new_capacity)
        # if size = 0, we do not need to copy the array
        if self.size > 0:
            # copy the elements
            for index in range(self.size):
                new_data[index] = self.data[index]
        # save the new static array to cover the data array
        self.data = new_data
        self.capacity = new_capacity

    def append(self, value: object) -> None:
        """
        This method adds a new value at the end of the dynamic array.
        If the internal storage is full, its capacity will be doubled.
        """
        # if size + 1 > capacity: double capacity
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        # change index to the end of the array, and set that value
        self.size += 1
        self.set_at_index(self.size - 1, value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        This method adds a new value at the specified index position.
        """
        # if index is invalid, raise the exception
        # in this case only, the new index could equal to size, ie add the value to the end
        if index < 0 or index > self.size:
            raise DynamicArrayException
        # if new size is larger than capacity: double capacity
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        # new size
        self.size += 1
        # from the end to the target index + 1 element, copy the old array
        for i in range(self.size - 1, index, -1):
            self.data[i] = self.data[i - 1]
        # change the target index element to the value
        self.data[index] = value

    def remove_at_index(self, index: int) -> None:
        """
        This method removes the element at the specified index.
        """
        # if the index is invalid, raise the exception
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        # if the size is strictly less than a quarter of capacity
        # resize the array capacity
        if self.size * 4 < self.capacity:
            if self.capacity > 10:
                if self.size * 2 > 10:
                    self.resize(self.size * 2)
                else:
                    self.resize(10)
            else:
                pass
        # copy the elements from index + 1 to the end
        # and paste them into elements from index to the end - 1
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        # change the last element to None
        self.data[self.size - 1] = None
        # reduce the size by one
        self.size -= 1

    def slice(self, start_index: int, size: int) -> object:
        """
        This method returns a new dynamic array with slice of the elements.
        """
        if start_index < 0 or start_index >= self.size or size < 0 or start_index + size > self.size:
            raise DynamicArrayException
        # create new dynamic array
        ret = DynamicArray()
        # save the target elements to the new array
        for index in range(start_index, start_index + size):
            ret.append(self.data[index])
        return ret

    def merge(self, second_da: object) -> None:
        """
        This method takes another dynamic array and appends all elements to the current one.
        """
        for index in range(second_da.length()):
            self.append(second_da[index])

    def map(self, map_func) -> object:
        """
        This method creates a new dynamic array where the value of each element
        is derived by map_func.
        """
        # create the new dynamic array
        ret = DynamicArray()
        # map the corrsponding elements to the new array
        for index in range(self.size):
            ret.append(map_func(self.data[index]))
        return ret

    def filter(self, filter_func) -> object:
        """
        This method creates a new dynamic array like filter().
        """
        # create the new dynamic array
        ret = DynamicArray()
        for index in range(self.size):
            # apply every element to the filter function
            if filter_func(self.data[index]):
                # if true, add the element to the new array
                ret.append(self.data[index])
        return ret

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        This method works similarly to the Python reduce() function to reduce the array to one elment.
        """
        # if the array is empty, return the value of the initializer
        if self.size == 0:
            return initializer
        # if there is no initializer
        if initializer is None:
            # x is the first value
            ans = self.data[0]
            for index in range(1, self.size):
                ans = reduce_func(ans, self.data[index])
        else:
            # we have an initializer
            ans = initializer
            for index in range(self.size):
                ans = reduce_func(ans, self.data[index])
        return ans

    def magic(self):
        for i in range(self.size, -1, -1):
            self.append(self.data[i])
            self.remove_at_index(i)
        return


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    This function received a sorted dynamic array,
    returns the mode or modes as a new dynamic array and the highest frequency in a tuple.
    """
    # create the new dynamic array to store the final answer
    ret = DynamicArray()
    # create a count array
    counts = DynamicArray()
    # set the flag to the first element
    pointer = arr[0]
    count, index = 0, 0
    frequency = 1
    # O(N) time complexity
    while index < arr.length():
        # if the element changed
        if arr[index] != pointer:
            # store the counts of the previous element to counts array
            counts.append(count)
            # if we have a new higher frequency, change the frequency
            if count > frequency:
                frequency = count
            # the flag now is the new element, and the new count is 1
            pointer = arr[index]
            count = 1
        else:
            # this element is the same with the previous one, count plus one
            count += 1
        # check the next element until the last one
        index += 1
    # for the last element, we still need to save this element's data
    counts.append(count)
    # and check if this is the new higher frequency
    if count > frequency:
        frequency = count
    # set the index to 0 of the dynamic array arr
    index = 0
    # check all the counts elements in counts
    for i in range(counts.length()):
        # this is the (index-1)th element in arr
        index += counts[i]
        # if this is the highest frequency element, add the related arr element to ret
        if counts[i] == frequency:
            ret.append(arr[index - 1])
    # return the answer as a tuple
    return (ret, frequency)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.resize(8)
    print(da.size, da.capacity, da.data)
    da.resize(2)
    print(da.size, da.capacity, da.data)
    da.resize(0)
    print(da.size, da.capacity, da.data)

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.append(1)
    print(da.size, da.capacity, da.data)
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.size)
    print(da.capacity)

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.size, da.capacity)
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.size, da.capacity)
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.size, da.capacity)

    for i in range(14):
        print("Before remove_at_index(): ", da.size, da.capacity, end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.size, da.capacity)

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 4, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot", "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
