import re
import sys


class BSTNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.parent = None
        self.value = value


def clear_value(value):
    first = 0

    while not value[first].isalpha():
        first += 1

    last = len(value) - 1
    while not value[last].isalpha():
        last -= 1

    return value[first: last + 1]


class BST:
    def __init__(self, compare, root=None, nil=None):
        self.root = root
        self.nil = nil
        self.compare = compare
        self.operations_occ = {'insert': 0, 'load': 0, 'delete': 0, 'find': 0,
                               'min': 0, 'max': 0, 'successor': 0, 'inorder': 0}
        self.num_elements = 0
        self.max_num_elements = 0

    def increment_num_elements(self):
        self.num_elements += 1
        if self.num_elements > self.max_num_elements:
            self.max_num_elements = self.num_elements

    def decrement_num_elements(self):
        self.num_elements -= 1

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def insert(self, value):
        try:
            value = clear_value(value)
        except IndexError:
            return

        self.operations_occ['insert'] += 1
        y = None
        x = self.root
        z = BSTNode(value)

        while x != self.nil:
            y = x
            if self.compare(z.value, x.value) == -1:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y is None:
            self.root = z
        elif self.compare(z.value, y.value) == -1:
            y.left = z
        else:
            y.right = z

        self.increment_num_elements()

    def load(self, f):
        self.operations_occ['load'] += 1
        try:
            with open(f) as file:
                text = file.read()
                words = re.split('[^a-zA-Z0-9_\']+', text)
                for word in words:
                    # print(word)
                    self.insert(word)
            return ""
        except FileNotFoundError:
            return "File doesn't exist\n"

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v != self.nil:
            v.parent = u.parent

    def remove(self, z):
        if z.left == self.nil:
            self.transplant(z, z.right)
        elif z.right == self.nil:
            self.transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            if y.parent != z:  # y isn't a right child of z node
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y

    def delete(self, value):
        self.operations_occ['delete'] += 1
        node = self._search(self.root, value)
        if node != self.nil:
            self.remove(node)
            self.decrement_num_elements()

    def _find(self, x, k):
        if x == self.nil:
            return 0
        if self.compare(k, x.value) == 0:
            return 1
        if self.compare(k, x.value) == -1:
            return self._find(x.left, k)
        else:
            return self._find(x.right, k)

    def find(self, k):
        self.operations_occ['find'] += 1
        print(self._find(self.root, k))

    def _search(self, x, k):
        if x == self.nil or self.compare(k, x.value) == 0:
            return x
        if self.compare(k, x.value) == -1:
            return self._search(x.left, k)
        else:
            return self._search(x.right, k)

    def _minimum(self, x):
        while x.left != self.nil:
            x = x.left
        return x

    def minimum(self):
        self.operations_occ['min'] += 1
        if self.root == self.nil:
            print()
        else:
            print(self._minimum(self.root).value)

    def _maximum(self, x):
        while x.right != self.nil:
            x = x.right
        return x

    def maximum(self):
        self.operations_occ['max'] += 1
        if self.root == self.nil:
            print()
        else:
            print(self._maximum(self.root).value)

    def _successor(self, x):
        if x.right != self.nil:
            return self._minimum(x.right)
        y = x.parent
        while y is not None and x == y.right:
            x = y
            y = y.parent
        return y

    def successor(self, value):
        self.operations_occ['successor'] += 1
        node = self._search(self.root, value)
        if node == self.nil:
            print()
        else:
            node_successor = self._successor(node)
            if node_successor is None:
                print()
            else:
                print(node_successor.value)

    def _inorder(self, x):
        if x != self.nil:
            self._inorder(x.left)
            print(x.value, end=" ")
            self._inorder(x.right)

    def inorder(self):
        self.operations_occ['inorder'] += 1
        self._inorder(self.root)
        print()
