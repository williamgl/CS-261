# Name: Gan Li
# OSU Email: ligan@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 - Part 2
# Due Date: 02/21/2022
# Description: Implement the AVL class by completing the add and remove methods.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Overrides string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super().str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self.root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the AVL tree.
        Then it checks if the tree is still AVL tree.
        If not, it rebalance the tree
        """
        # This method MUST be re-implemented
        # create the new node with the value
        node = AVLNode(value)
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
                        node.parent = cur
                        # break the while loop
                        cur = False
                # if the new node's value is large or equal to the cur's value
                elif value > cur.value:
                    # if the cur has a right child
                    # set the right child to cur and then compare its value with the new value
                    if cur.right:
                        cur = cur.right
                    # until there is no right value
                    # i.e. this new node will be the largest in this subtree
                    else:
                        # make the new node the right child of cur node
                        cur.right = node
                        node.parent = cur
                        # break the while loop
                        cur = False
                else:
                    return
            # now the new node is added
            if self.is_valid_avl():
                return
            else:
                # rebalance from the new node
                while node:
                    # rebalance until the root
                    self.rebalance(node)
                    node = node.parent

    def remove(self, value: object) -> bool:
        """
        This method removes the value from the tree.
        It returns True if the value is removed; otherwise returns False.
        """
        # check whether the target value was found or not
        # if not, return False
        if not self.contains(value):
            return False
        # Using an inside function to breadth first search the BST tree
        # Step 1 - Perform standard BST delete
        node_changed = AVLNode(0)
        def bfs(root, key):
            nonlocal node_changed
            # if the root is None, return None
            if not root:
                return root
            # if the target value is larger, we bfs the left subtree
            if key < root.value:
                root.left = bfs(root.left, key)
            # if the target value is smaller, we bfs the right subtree
            elif key > root.value:
                root.right = bfs(root.right, key)
            # if the target value equals to the key value, we remove this node
            else:
                # we have three scenarios
                # scenario 1: the node has both left and right children
                if root.left and root.right:
                    # here we have two sub-scenarios
                    # scenarios 1.1: we have a leftmost node in the right subtree
                    if root.right.left:
                        leftmost = root.right.left
                        # find leftmost node and its parent node
                        while leftmost.left:
                            leftmost = leftmost.left
                        leftmostParent = leftmost.parent
                        node_changed = leftmost
                        # change the leftmost node's parent node' left node to its right subtree
                        # since we are using this node to replace the target node
                        if leftmost.right:
                            leftmostParent.left = leftmost.right
                            leftmost.right.parent = leftmostParent
                        else:
                            leftmostParent.left = None
                        # change the left and right of the leftmost node to the target node's left and right
                        root.value = leftmost.value
                    # scenario 1.2: the right subtree does not have a left subtree
                    else:
                        # replace the target node with its right node
                        root.right.left = root.left
                        root.left.parent = root.right
                        root.right.parent = root.parent
                        root = root.right
                        node_changed = root.left
                # scenario 2: the subtree of the target node only have one child
                # because this is an AVL tree, this child must be a leaf, and this node must be the root of this subtree
                elif root.left:
                    root.value = root.left.value
                    node_changed = root.left
                    root.left = None
                elif root.right:
                    root.value = root.right.value
                    node_changed = root.right
                    root.right = None
                # scenario 3: the target node is a leaf
                else:
                    if not root.parent:
                        self.make_empty()
                    else:
                        node_changed = root
                    root = None
            return root
        self.root = bfs(self.root, value)
        if not node_changed:
            return True
        target = node_changed.parent
        while target:
            self.rebalance(target)
            target = target.parent
        return True

    # ------------------------------------------------------------------ #

    ################################################################
    # It's highly recommended, though not required,
    # to implement these methods for balancing the AVL Tree.
    ################################################################

    def balance_factor(self, node):
        """
        This method returns the balance factor of a node.
        """
        return self.get_height(node.right) - self.get_height(node.left)

    def update_height(self, node):
        """update all nodes' heights"""
        if node.left and node.right:
            node.height = max(node.left.height, node.right.height) + 1
        elif node.left:
            node.height = node.left.height + 1
        elif node.right:
            node.height = node.right.height + 1
        else:
            node.height = 0
        """
        # update the parent and ancestors' heights
        while node.parent:
            parent = node.parent
            if parent.left and parent.right:
                parent.height = max(parent.left.height, parent.right.height) + 1
            else:
                parent.height = node.height + 1
            node = parent
        # when it is the root, the while loop breaks
        # we do the update again for the root
        if node.left and node.right:
            node.height = max(node.left.height, node.right.height) + 1
        elif node.left:
            node.height = node.left.height + 1
        else:
            node.height = node.right.height + 1
        """

    def get_height(self, node):
        if not node:
            return -1
        return node.height

    def get_min(self, node):
        if not node or not node.left:
            return node
        return self.get_min(node.left)

    def rotate_left(self, node):
        """
        This method does a left rotation at the node.
        :return: The new root node
        """
        # There must be at least one right node.
        # node.left would not be changed
        temp = node.right
        node.right = temp.left
        if node.right:
            node.right.parent = node
        temp.left = node
        node.parent = temp
        self.update_height(node)
        self.update_height(temp)
        return temp

    def rotate_right(self, node):
        """
        This method does a right rotation at the node.
        :return: The new root node
        """
        # There mus be at least one left node.
        # node.right would not be changed
        temp = node.left
        node.left = temp.right
        if node.left:
            node.left.parent = node
        temp.right = node
        node.parent = temp
        self.update_height(node)
        self.update_height(temp)
        return temp

    def rebalance(self, node):
        """This method rebalance the target node"""
        if self.balance_factor(node) == -2:
            # the L-R case
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
                node.left.parent = node
            # the second part of L-R case, or the L-L case
            newParent = node.parent
            newRoot = self.rotate_right(node)
            newRoot.parent = newParent
            if not newParent:
                self.root = newRoot
                newRoot.parent = None
                return
            if newParent.left == node:
                newParent.left = newRoot
            else:
                newParent.right = newRoot
        elif self.balance_factor(node) == 2:
            # the R-L case
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
                node.right.parent = node
            # the second part of R-L case, or the R-R case
            newParent = node.parent
            newRoot = self.rotate_left(node)
            newRoot.parent = newParent
            if not newParent:
                self.root = newRoot
                newRoot.parent = None
                return
            if newParent.left == node:
                newParent.left = newRoot
            else:
                newParent.right = newRoot
        else:
            self.update_height(node)

    # ------------------------------------------------------------------ #

    ################################################################
    # Use the methods as a starting point if you'd like to override.
    # Otherwise, the AVL can simply call any BST method.
    ################################################################

    '''
    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        return super().contains(value)

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        return super().inorder_traversal()

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        return super().find_min()

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        return super().find_max()

    def is_empty(self) -> bool:
        """
        TODO: Write your implementation
        """
        return super().is_empty()

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        super().make_empty()
    '''

# ------------------- BASIC TESTING -----------------------------------------

'''
if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(3):
        case = list(set(random.randrange(1, 20000) for _ in range(9)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', tree, tree.root.value)
        tree.remove(tree.root.value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
'''