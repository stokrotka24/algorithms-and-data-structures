import sys


class PQelem:
    def __init__(self, value, priority):
        if priority < 0:
            raise Exception("Priority must be nonnegative!")
        self.value = value
        self.priority = priority

    def print(self):
        print(f"({self.value}, {self.priority})", end=" ")


def _parent(index):
    return (index - 1) // 2


def _left(index):
    return 2 * index + 1


def _right(index):
    return 2 * index + 2


class PriorityQueue:
    def __init__(self, compare):
        self.elements = []
        self.last_valid_index = -1
        self.compare = compare

    def insert(self, x, p):
        self.elements.append(PQelem(float('inf'), float('inf')))
        self.last_valid_index += 1
        i = self.last_valid_index

        while i > 0 and self.compare(self.elements[_parent(i)].priority, p) == -1:
            self.elements[i] = self.elements[_parent(i)]
            i = _parent(i)

        pqelem = PQelem(x, p)
        self.elements[i] = pqelem

    def empty(self):
        if self.last_valid_index == -1:
            print(1)
        else:
            print(0)

    def empty_val(self):
        if self.last_valid_index == -1:
            return 1
        else:
            return 0

    def top(self):
        if self.last_valid_index >= 0:
            print(self.elements[0].value)
        else:
            print()

    def _heapify(self, i):
        left = _left(i)
        right = _right(i)

        highest = i
        if left <= self.last_valid_index and self.compare(self.elements[left].priority, self.elements[i].priority) == 1:
            highest = left
        if right <= self.last_valid_index and self.compare(self.elements[right].priority,
                                                           self.elements[highest].priority) == 1:
            highest = right

        if highest != i:
            self.elements[highest], self.elements[i] = self.elements[i], self.elements[highest]
            self._heapify(highest)

    def pop(self):
        if self.last_valid_index >= 0:
            print(self.elements[0].value)
            self.elements[0] = self.elements[self.last_valid_index]
            self.last_valid_index -= 1
            self._heapify(0)
        else:
            print()

    def pop_val(self):
        popped_value = None
        if self.last_valid_index >= 0:
            popped_value = self.elements[0].value
            self.elements[0] = self.elements[self.last_valid_index]
            self.last_valid_index -= 1
            self._heapify(0)
        return popped_value

    def priority(self, x, p):
        i = 0
        while i <= self.last_valid_index:
            if self.elements[i].value == x:
                if self.compare(p, self.elements[i].priority) == 1:
                    self.elements[i].priority = p
                    j = i

                    while j > 0 and self.compare(self.elements[_parent(j)].priority, p) == -1:
                        self.elements[j], self.elements[_parent(j)] = self.elements[_parent(j)], self.elements[j]
                        j = _parent(j)
            i += 1

    def contains(self, x):
        i = 0
        while i <= self.last_valid_index:
            if self.elements[i].value == x:
                return True
            i += 1
        return False

    def print(self):
        i = 0
        while i <= self.last_valid_index:
            self.elements[i].print()
            i += 1
        print()
