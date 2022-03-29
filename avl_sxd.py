# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


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
                        node.parent = cur
                        # break the while loop
                        cur = False
            # now the new node is added
            if self.is_valid_avl():
                return
            else:
                # the new avl tree needs a rebalance
                # rebalance from the parent of the new node
                cur = node
                while cur:
                    # rebalance until the root
                    self.rebalance(cur)
                    cur = cur.parent

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        # This method MUST be re-implemented
        pass

    # ------------------------------------------------------------------ #

    ################################################################
    # It's highly recommended, though not required,
    # to implement these methods for balancing the AVL Tree.
    ################################################################

    def balance_factor(self, node):
        """
        This method returns the balance factor of a node.
        """
        if node.left and node.right:
            return node.right.height - node.left.height
        elif node.left:
            return -1 - node.left.height
        elif node.right:
            return node.right.height + 1
        else:
            # this node is a leaf
            return 0

    def update_height(self, node):
        print('update_height, %d' % node.value)
        """update all nodes' heights"""
        if node.left and node.right:
            node.height = max(node.left.height, node.right.height) + 1
        elif node.left:
            node.height = node.left.height + 1
        elif node.right:
            node.height = node.right.height + 1
        else:
            node.height = 0
        # update the parent and ancestors' heights
        while node.parent:
            print('node.parent, %d' % node.parent.value)
            parent = node.parent
            if parent.left and parent.right:
                parent.height = max(parent.left.height, parent.right.height) + 1
            else:
                parent.height = node.height + 1
            node = parent
        # when it is the root, the while loop is break
        # we do the update again for the root
        if node.left and node.right:
            node.height = max(node.left.height, node.right.height) + 1
        elif node.left:
            node.height = node.left.height + 1
        else:
            node.height = node.right.height + 1

    def rotate_left(self, node):
        """
        This method does a left rotation at the node.
        :return: The new root node
        """
        # There must be at least one right node.
        # node.left would not be changed
        print('rotate_left, %d' % node.value)
        temp = node.right
        temp.parent = node.parent
        node.right = temp.left
        if node.right:
            node.right.parent = node
        temp.left = node
        node.parent = temp
        self.update_height(node)
        return temp

    def rotate_right(self, node):
        """
        This method does a right rotation at the node.
        :return: The new root node
        """
        print('rotate_right, %d' % node.value)
        # There mus be at least one left node.
        # node.right would not be changed
        temp = node.left
        temp.parent = node.parent
        node.left = temp.right
        if node.left:
            node.left.parent = node
        temp.right = node
        node.parent = temp
        self.update_height(node)
        return temp

    def rebalance(self, node):
        """This method rebalance the target node"""
        print('rebalance, %d' % node.value)
        if self.balance_factor(node) == -2:
            # the L-R case
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
                node.left.parent = node
            # the second part of L-R case, or the L-L case
            newNode = self.rotate_right(node)
            newNode.parent = node.parent
            if node.parent.left == node:
                node.parent.left = newNode
            else:
                node.parent.right = newNode
        elif self.balance_factor(node) == 2:
            # the R-L case
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
                node.right.parent = node
            # the second part of R-L case, or the R-R case
            newNode = self.rotate_left(node)
            newNode.parent = node.parent
            if node.parent.left == node:
                node.parent.left = newNode
            else:
                node.parent.right = newNode
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

case = (1, 2, 3)
tree = AVL(case)