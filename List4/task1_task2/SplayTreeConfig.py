from BSTConfig import BSTNode, BST, clear_value


class SplayNode(BSTNode):
    def __init__(self, value):
        BSTNode.__init__(self, value)


class SplayTree(BST):
    def __init__(self, compare):
        BST.__init__(self, compare)

    def splay(self, x):
        while x.parent is not None:
            if x.parent.parent is None:
                if x == x.parent.left:
                    # zig rotation
                    self.right_rotate(x.parent)
                else:
                    # zag rotation
                    self.left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.right_rotate(x.parent.parent)
                self.right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.left_rotate(x.parent.parent)
                self.left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.left_rotate(x.parent)
                self.right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.right_rotate(x.parent)
                self.left_rotate(x.parent)

    def insert(self, value):
        try:
            value = clear_value(value)
        except IndexError:
            return

        self.operations_occ['insert'] += 1
        y = None
        x = self.root
        z = SplayNode(value)

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

        self.splay(z)
        self.increment_num_elements()

    def delete(self, value):
        self.operations_occ['delete'] += 1
        node = self._search(self.root, value)
        if node != self.nil:
            self.splay(node)
            self.remove(node)
            self.decrement_num_elements()

    def find(self, k):
        self.operations_occ['find'] += 1
        x = self._search(self.root, k)
        if x != self.nil:
            self.splay(x)
            print(1)
        else:
            print(0)

    def successor(self, value):
        self.operations_occ['successor'] += 1
        node = self._search(self.root, value)
        if node == self.nil:
            print()
        else:
            self.splay(node)
            node_successor = self._successor(node)
            if node_successor is None:
                print()
            else:
                print(node_successor.value)
