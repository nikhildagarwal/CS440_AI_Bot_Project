from collections import deque


class Node:
    def __init__(self, tup):
        self.loc = tup
        self.prev = None
        self.next = []


class ANode:
    def __init__(self, tup, cost, heuristic, prev):
        self.loc = tup
        self.g = cost
        self.h = heuristic
        self.f = cost + heuristic
        self.prev = prev

    def __lt__(self, other):
        if isinstance(other,ANode):
            return self.f < other.f
        return TypeError

    def __eq__(self, other):
        if isinstance(other, ANode):
            return self.loc == other.loc
        return TypeError

    def __hash__(self):
        return hash(self.loc)


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
