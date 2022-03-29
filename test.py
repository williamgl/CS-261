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

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        self.data[index] = value

    def dynArrayAddAt(self, index: int, value: object) -> None:
        """
        This method adds an element at a particular index in the DA.
        """
        # if index is invalid, raise the exception
        if index < 0 or index > self.size:
            raise DynamicArrayException
        # if new size is larger than capacity: double capacity
        if self.size == self.capacity:
            # creating a new dynamic array
            new_data = StaticArray(self.capacity * 2)
            for index in range(self.size):
                new_data[index] = self.data[index]
            # save the new static array to cover the data array
            self.data = new_data
            self.capacity *= 2
        # new size
        self.size += 1
        # from the end to the target index + 1 element, copy the old array
        for i in range(self.size - 1, index, -1):
            self.data[i] = self.data[i - 1]
        # change the target index element to the value
        self.data[index] = value
        return

    def remove_at_index(self, index: int) -> None:
        """
        This method removes the element at the specified index.
        """
        # if the index is invalid, raise the exception
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        # copy the elements from index + 1 to the end
        # and paste them into elements from index to the end - 1
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        # change the last element to None
        self.data[self.size - 1] = None
        # reduce the size by one
        self.size -= 1
