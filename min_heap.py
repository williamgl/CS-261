# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 02/28/2022
# Description: I will implement the MinHeap class by completing the following methods:
#               is_empty, add, get_min, remove_min, build_heap, size, clear, heapsort.

# Import DynamicArray from Assignment 2
from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self.heap[i] for i in range(self.heap.length())]
        return 'HEAP ' + str(heap_data)

    def is_empty(self) -> bool:
        """
        This method returns True if the heap is empty. Otherwise, it returns False.
        """
        # self.heap is a dynamic array. We could use the is_empty method of DA class.
        return self.heap.is_empty()

    def add(self, node: object) -> None:
        """
        This method adds a new object to the MinHeap while maintaining heap property.
        """
        # first, add the node value to the end of the heap
        self.heap.append(node)
        # find i
        index = self.heap.length() - 1
        parent_index = index
        # while this is not the beginning
        while parent_index != 0:
            # compute the element's parent index
            parent_index = (parent_index - 1) // 2
            # if the parent value is greater, swap the elements
            if self.heap.get_at_index(parent_index) > node:
                self.swap(index, parent_index)
                # update the target element index
                index = parent_index

    def get_min(self) -> object:
        """
        This method return the minimum key without removing it.
        If the heap is empty, raise the exception
        """
        if self.is_empty():
            raise MinHeapException
        return self.heap.get_at_index(0)

    def swap(self, index1, index2):
        value1, value2 = self.heap.get_at_index(index1), self.heap.get_at_index(index2)
        self.heap.set_at_index(index1, value2)
        self.heap.set_at_index(index2, value1)

    def remove_min(self) -> object:
        """
        This method return the min key and removes it.
        If the heap is empty, raise the exception.
        """
        if self.is_empty():
            raise MinHeapException
        ans = self.get_min()
        # get the last element index
        index = self.size() - 1
        # get the last element value
        target = self.heap.get_at_index(index)
        # set the top value to target
        self.heap.set_at_index(0, target)
        # remove the last element
        self.heap.remove_at_index(index)
        # if after removal, the heap is empty
        if self.is_empty():
            return ans
        # relocate the target element
        index = 0
        while index < self.size():
            # create the children indices and elements values
            l_child, r_child = index * 2 + 1, index * 2 + 2
            # when the element does not have children
            if l_child >= self.size():
                # it is at its correct place
                return ans
            elif r_child == self.size():
                # if it only has left child, i.e. its left child is the end of the list
                left = self.heap.get_at_index(l_child)
                if target < left:
                    # if it is at its correct place
                    return ans
                else:
                    # swap this element with its left node
                    self.swap(l_child, index)
                    return ans
            # when both children exit
            left, right = self.heap.get_at_index(l_child), self.heap.get_at_index(r_child)
            if target < left and target < right:
                # the target element reaches its correct place, break the while loop
                return ans
            elif left <= right:
                # the element needs to swap with its left child
                self.swap(l_child, index)
                index = l_child
            else:
                # the element needs to swap with its right child
                self.swap(r_child, index)
                index = r_child

    def build_heap(self, da: DynamicArray) -> None:
        """
        This method receives a dynamic array and build a proper MinHeap from them.
        """
        # first, replace the heap with da
        def copy(x):
            return x
        self.heap = da.map(copy)
        if self.is_empty():
            return
        count = 0
        while 2 ** count < self.size():
            # index points to the first node that has at least a child
            index = self.size() // 2 - 1
            while index >= 0:
                l_index, r_index = index * 2 + 1, index * 2 + 2
                # if there is only one left child
                if r_index == self.size():
                    if self.heap[index] > self.heap[l_index]:
                        self.swap(index, l_index)
                elif self.heap[index] > self.heap[l_index] or \
                        self.heap[index] > self.heap[r_index]:
                    if self.heap[l_index] <= self.heap[r_index]:
                        self.swap(index, l_index)
                    else:
                        self.swap(index, r_index)
                else:
                    pass
                index -= 1
            count += 1

    def size(self) -> int:
        """
        This method return the number of items currently stored in the heap
        """
        return self.heap.length()

    def clear(self) -> None:
        """
        This method clears the contents of the heap.
        """
        self.heap = DynamicArray()
        return


def heapsort(da: DynamicArray) -> None:
    """
    This function sorts a DA in non-ascending order using the Heapsort algorithm.
    """
    # counter k point to the last element
    k = da.length() - 1
    # create a heap of da
    heap = MinHeap()
    heap.build_heap(da)
    while k >= 0:
        # set the kth element to the min of the heap
        da[k] = heap.remove_min()
        # now the heap is a new heap without the min
        # the new head is the new min
        k -= 1

'''
# BASIC TESTING
if __name__ == '__main__':
    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap()
    h.heap = DynamicArray([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da[0] = 500
    print(da)
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
'''