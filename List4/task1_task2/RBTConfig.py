import enum

from BSTConfig import BSTNode, BST, clear_value


class Colors(enum.Enum):
    RED = 1
    BLACK = 2


class RBTNode(BSTNode):
    def __init__(self, value, color=None):
        self.color = color
        BSTNode.__init__(self, value)


class RBT(BST):
    def __init__(self, compare):
        nil = RBTNode(None, Colors.BLACK)
        root = nil
        BST.__init__(self, compare, root, nil)

    def insert_fixup(self, z):
        while z.parent is not None and z.parent.color == Colors.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # uncle

                if y.color == Colors.RED:  # case 1
                    z.parent.color = Colors.BLACK
                    y.color = Colors.BLACK
                    z.parent.parent.color = Colors.RED
                    z = z.parent.parent
                else:  # case 2 or case 3
                    if z == z.parent.right:  # case 2
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = Colors.BLACK
                    z.parent.parent.color = Colors.RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left

                if y.color == Colors.RED:
                    z.parent.color = Colors.BLACK
                    y.color = Colors.BLACK
                    z.parent.parent.color = Colors.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = Colors.BLACK
                    z.parent.parent.color = Colors.RED
                    self.left_rotate(z.parent.parent)
        self.root.color = Colors.BLACK

    def insert(self, value):
        try:
            value = clear_value(value)
        except IndexError:
            return

        self.operations_occ['insert'] += 1
        y = None
        x = self.root
        z = RBTNode(value)

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

        z.left = self.nil
        z.right = self.nil
        z.color = Colors.RED
        self.insert_fixup(z)
        self.increment_num_elements()

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete_fixup(self, x):
        while x != self.root and x.color == Colors.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Colors.RED:
                    w.color = Colors.BLACK
                    x.parent.color = Colors.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == Colors.BLACK and w.right.color == Colors.BLACK:
                    w.color = Colors.RED
                    x = x.parent
                else:
                    if w.right.color == Colors.BLACK:
                        w.left.color = Colors.BLACK
                        w.color = Colors.RED
                        self.right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = Colors.BLACK
                    w.right.color = Colors.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Colors.RED:
                    w.color = Colors.BLACK
                    x.parent.color = Colors.RED
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.left.color == Colors.BLACK and w.right.color == Colors.BLACK:
                    w.color = Colors.RED
                    x = x.parent
                else:
                    if w.left.color == Colors.BLACK:
                        w.right.color = Colors.BLACK
                        w.color = Colors.RED
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = Colors.BLACK
                    w.left.color = Colors.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Colors.BLACK

    def remove(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:  # y is a right child of z node
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == Colors.BLACK:
            self.delete_fixup(x)




