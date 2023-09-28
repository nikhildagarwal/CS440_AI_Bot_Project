import random
from coordinate import Coordinate


class Ship:
    def __init__(self, dim):
        """
        Builds the layout of ship object
        :param dim: size of the ship layout (dim x dim grid)
        """
        self.layout = initialize_grid(dim)
        self.layout[generate_random(0, dim - 1)][generate_random(0, dim - 1)] = 0

    def print_out(self):
        """
        Prints the layout of our ship
        :return: None
        """
        for row in self.layout:
            print(row)


def generate_random(a, b):
    """
    Generates random number between a and b (inclusive)
    :param a: lower number
    :param b: higher number
    :return: random number
    """
    return random.randint(a, b)


def initialize_grid(dim):
    """
    Creates an NxN 2D list and populates it with 1's
    :param dim: dimension of grid
    :return: 2D list populated with 1's
    """
    layout = []
    for i in range(dim):
        row = []
        for j in range(dim):
            row.append(1)
        layout.append(row)
    return layout
