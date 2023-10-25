class ANode:
    """
    Node object to hold location of each cell, hold the current cost that it took to reach the cell,
        the new heuristic value from this current cell and the cost plus heuristic value.
    Also points to the previous node in the chain so that we can extract paths from the node
    """
    def __init__(self, tup, cost, heuristic, prev):
        """
        Init method for node
        :param tup: location of cell as a tuple Ex: (i,j)
        :param cost: cost to reach this cell
        :param heuristic: heuristic value
        :param prev: pointer to previous Node
        """
        self.loc = tup
        self.g = cost
        self.h = heuristic
        self.f = cost + heuristic
        self.prev = prev

    def __lt__(self, other):
        """
        Override of 'less than' function
        :param other: other object
        :return: compare the (cost + heuristic) values of each Anode object
        """
        if isinstance(other,ANode):
            return self.f < other.f
        return TypeError

    def __eq__(self, other):
        """
        Override of equals method
        :param other: other Anode object
        :return: true if location tuples match, false otherwise
        """
        if isinstance(other, ANode):
            return self.loc == other.loc
        return TypeError

    def __hash__(self):
        """
        Override of Anode object
        :return: hash by tuple element
        """
        return hash(self.loc)
