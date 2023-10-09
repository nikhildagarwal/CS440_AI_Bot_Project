from collections import deque


class Node:
    def __init__(self, tup):
        self.loc = tup
        self.prev = None
        self.next = []


class Fringe:
    def __init__(self, start_node):
        self.queue = deque([start_node])
        self.visited = {0}
        self.visited.remove(0)
        self.root = Node(start_node)

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return self.queue.popleft()

    def add(self, curr_node, new_node):
        curr_node.next.append(new_node)
        new_node.prev = curr_node
        self.queue.append(new_node)
