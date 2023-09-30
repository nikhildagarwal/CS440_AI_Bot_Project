from collections import deque


class Queue:
    def __init__(self):
        self.queue = deque()

    def is_empty(self):
        return len(self.queue) == 0

    def add(self, node):
        self.queue.append(node)

    def poll(self):
        return self.queue.popleft()


class Set:
    def __init__(self):
        self.set = {0}

    def add(self, node):
        self.set.add(node)

    def remove(self, node):
        self.set.remove(node)

    def is_empty(self):
        return len(self.set) == 1

    def print_out(self):
        print(self.set)


class Node:
    def __init__(self, tup):
        self.loc = tup
        self.next_nodes = Set()
        self.prev = None


class Fringe:
    def __init__(self, init_loc):
        self.visited = {0}
        self.root = Node(init_loc)
        self.queue = Queue()
        self.queue.add(self.root)

    def pop(self):
        return self.queue.poll()

    def add(self, new_node, old_node, tup):
        self.queue.add(new_node)
        self.visited.add(tup)
        old_node.next_nodes.add(new_node)
        new_node.prev = old_node




