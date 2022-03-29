# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3 Part 1
# Due Date: Feb 7, 2022
# Description: singly linked list implementation by completing eight methods.

from SLNode import SLNode


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with front and back sentinels
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = SLNode(None)
        self.tail = SLNode(None)
        self.head.next = self.tail

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        if self.head.next != self.tail:
            cur = self.head.next.next
            out = out + str(self.head.next.value)
            while cur != self.tail:
                out = out + ' -> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            length += 1
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head.next == self.tail

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        This method adds a new node at the beginning of the list.
        """
        # save the first data in the list as temp
        # if there is no data in the list yet, save tail as temp
        temp = self.head.next
        # create the new node using the given value and save temp as its next node
        node = SLNode(value, temp)
        # replace head.next with the new node
        self.head.next = node

    def insert_back(self, value: object) -> None:
        """
        This method adds a new node at the end of the list.
        """
        # create the new node using the given value and tail as its next node
        node = SLNode(value, self.tail)
        # find the last data and save it as cur
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
        # save the next node of the last data to the new node
        cur.next = node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        This method adds a new value at the specified index position.
        """
        # if the provided index is invalid, raise "SLLException"
        if index < 0 or index > self.length():
            raise SLLException
        # find the target node before the index
        cur = self.head
        while index != 0:
            cur = cur.next
            index -= 1
        # create the new node with the given value and the cur.next node
        node = SLNode(value, cur.next)
        # replace cur.next with the new node
        cur.next = node

    def remove_at_index(self, index: int) -> None:
        """
        This method removes the node at the specified index fom the list
        """
        # if the provided index is invalid, raise "SLLException"
        if index < 0 or index >= self.length():
            raise SLLException
        # find the target node before the index
        cur = self.head
        while index != 0:
            cur = cur.next
            index -= 1
        # save the next node of the target node as temp
        temp = cur.next.next
        # replace cur.next with temp
        cur.next = temp

    def remove(self, value: object) -> bool:
        """
        This method traverses the list from the beginning to the end
        and removes the first node in the list that matches the given value.
        It returns True if a node was removed and False otherwise.
        """
        cur = self.head
        while cur.next:
            # if the target value found
            if cur.next.value == value:
                # remove the next node when the value matches
                # and then return True
                temp = cur.next.next
                cur.next = temp
                return True
            # try the next node until the tail
            cur = cur.next
        # reach to the tail, no such value was found
        return False

    def count(self, value: object) -> int:
        """
        This method counts the number of elements in the list that match the given value.
        """
        # set the count variable to 0
        count = 0
        cur = self.head
        while cur.next:
            # if the target value found, count = count + 1
            if cur.next.value == value:
                count += 1
            cur = cur.next
        return count

    def find(self, value: object) -> bool:
        """
        This method works like 'in' to determine whether the given value are in the list or not.
        """
        cur = self.head
        while cur.next:
            # if the target value found, return True
            if cur.next.value == value:
                return True
            cur = cur.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        This method returns a new Linked List that contains the requested number of nodes
        from the original list starting with the node located at the given index.
        """
        # if the provided index is invalid, or there are not enough nodes between the start index
        # and the end of the list to make such a slice, raise "SLLException"
        if start_index < 0 or start_index >= self.length() or start_index + size > self.length() or size < 0:
            raise SLLException
        cur = self.head
        # find the target node before the given index
        while start_index != 0:
            cur = cur.next
            start_index -= 1
        # create the answer linked list
        slicedLL = LinkedList()
        # add size numbers to the answer
        while size > 0:
            cur = cur.next
            slicedLL.insert_back(cur.value)
            size -= 1
        return slicedLL


if __name__ == '__main__':

    print('\n# insert_front example 1')
    lst = LinkedList()
    print(lst)
    lst.insert_front('A')
    lst.insert_front('B')
    lst.insert_front('C')
    print(lst)


    print('\n# insert_back example 1')
    lst = LinkedList()
    print(lst)
    lst.insert_back('C')
    lst.insert_back('B')
    lst.insert_back('A')
    print(lst)


    print('\n# insert_at_index example 1')
    lst = LinkedList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))


    print('\n# remove_at_index example 1')
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(lst)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))
    print(lst)

    print('\n# remove example 1')
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(lst)
    for value in [7, 3, 3, 3, 3]:
        print(lst.remove(value), lst.length(), lst)


    print('\n# count example 1')
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))


    print('\n# find example 1')
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Clause"])
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Clause"))


    print('\n# slice example 1')
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print(lst, ll_slice, sep="\n")
    ll_slice.remove_at_index(0)
    print(lst, ll_slice, sep="\n")


    print('\n# slice example 2')
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", lst.slice(index, size))
        except:
            print(" --- exception occurred.")

