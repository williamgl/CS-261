# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 - Part 1
# Due Date: 02/21/2022
# Description: Implement the BST class by completing the following methods:
#               add, remove, contains, inorder traversal, find min,
#               find max, is empty, make empty.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None  # pointer to root of left subtree
        self.right = None  # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of BST in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self.str_helper(self.root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self.str_helper(node.left, values)
        self.str_helper(node.right, values)

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree.
        If the value is already in the tree, simply add the new value to the right subtree.
        """
        # create the new node with the value
        node = BSTNode(value)
        # if the tree is empty, set the node as the root
        if self.is_empty():
            self.root = node
        # if the tree has a root
        else:
            # set the root as cur
            cur = self.root
            while cur:
                # if the new node's value is less than the cur's value
                if value < cur.value:
                    # if the cur has a left child
                    # set the left child to cur and then compare its value with the new value
                    if cur.left:
                        cur = cur.left
                    # until there is no left value
                    # i.e. this new node will be the smallest in this subtree
                    else:
                        # make the new node the left child of cur node
                        cur.left = node
                        return
                # if the new node's value is large or equal to the cur's value
                else:
                    # if the cur has a right child
                    # set the right child to cur and then compare its value with the new value
                    if cur.right:
                        cur = cur.right
                    # until there is no right value
                    # i.e. this new node will be the largest in this subtree
                    else:
                        # make the new node the right child of cur node
                        cur.right = node
                        return

    def remove(self, value: object) -> bool:
        """
        This method removes the value from the tree.
        It returns True if the value is removed; otherwise returns False.
        """
        # check whether the target value was found or not
        # if not, return False
        if not self.contains(value):
            return False
        # Using an inside function to breadth first search the BST
        def bfs(root, key):
            # if the root of this subtree is None, return None
            if not root:
                return None
            # if the target value is smaller than the key value, we bfs the right subtree
            if root.value < key:
                root.right = bfs(root.right, key)
            # if the target value is larger than the key value, we bfs the left subtree
            elif root.value > key:
                root.left = bfs(root.left, key)
            # if the target value equals to the key value, we remove this node
            else:
                # we have three scenarios
                # scenario 1: the node has both left and right children
                if root.left and root.right:
                    # here we have two sub-scenarios
                    # scenarios 1.1: we have a leftmost node in the right subtree
                    if root.right.left:
                        leftmost = root.right.left
                        leftmostParent = root.right
                        # find leftmost node and its parent node
                        while leftmost.left:
                            leftmost = leftmost.left
                            leftmostParent = leftmostParent.left
                        # change the leftmost node's parent node' left node to None
                        # since we are using this node to replace the target node
                        leftmostParent.left = leftmost.right
                        # change the left and right of the leftmost node to the target node's left and right
                        leftmost.left, leftmost.right = root.left, root.right
                        # replace the target node with the leftmost node
                        root = leftmost
                    # scenario 1.2: the right subtree does not have a left subtree
                    else:
                        # replace the target node with its right node
                        root.right.left = root.left
                        root = root.right
                # scenario 2: the subtree of the target node only have one child
                elif root.left:
                    root = root.left
                elif root.right:
                    root = root.right
                # scenario 3: the target node is a leaf
                else:
                    root = None
            return root
        # update the whole BST
        self.root = bfs(self.root, value)
        return True

    def contains(self, value: object) -> bool:
        """
        This method check if the key value is in the BST.
        """
        # using an inside function to breadth first search the BST
        def bfs(node, val):
            if not node:
                return False
            if node.value == val:
                return True
            else:
                return bfs(node.left, val) or bfs(node.right, val)
        return bfs(self.root, value)

    def inorder_traversal(self) -> Queue:
        """
        This method performs an inorder traversal of the BST and return the results in a queue.
        """
        # create the answer queue
        answer = Queue()
        # using an inside function to depth first search the BST
        def dfs(node, ans):
            if not node:
                return
            dfs(node.left, ans)
            ans.enqueue(node.value)
            dfs(node.right, ans)
        dfs(self.root, answer)
        return answer

    def find_min(self) -> object:
        """
        This method returns the lowest value in the tree.
        """
        if self.is_empty():
            return None
        # find the leftmost node
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.value

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree.
        """
        if self.is_empty():
            return None
        # find the rightmost node
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.value

    def is_empty(self) -> bool:
        """
        This method returns True if the tree is empty.
        Otherwise, return False
        """
        # the BST is empty when the root is None
        return self.root is None

    def make_empty(self) -> None:
        """
        This method removes all the nodes from the tree.
        """
        # simply change the root node to None
        self.root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        print('INPUT  :', tree, tree.root.value)
        tree.remove(tree.root.value)
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
