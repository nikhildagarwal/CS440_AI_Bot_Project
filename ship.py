import random


class Ship:
    def __init__(self, dim):
        """
        Builds the layout of ship object
        :param dim: size of the ship layout (dim x dim grid)
        """
        self.robot_loc = None
        self.fire_loc = None
        self.button_loc = None
        self.dim = dim
        self.layout, self.blocked = initialize_grid(dim)
        open_first_block(dim, self.layout, self.blocked)
        self.final_state = False
        while not self.final_state:
            next_open_set = search_next_open(self.layout, self.blocked, dim)
            if len(next_open_set) == 0:
                self.final_state = True
            else:
                r_index = generate_random(0, len(next_open_set) - 1)
                tup = next_open_set[r_index]
                self.blocked.remove(tup)
                self.layout[tup[0]][tup[1]] = 0
        dead_ends = find_dead_ends(self.layout, dim)
        n_purge = get_n_purge(len(dead_ends))
        purge_half(dead_ends, self.layout, dim, n_purge)

    def init_environment(self, bot):
        """
        initializes fire, safety button, and bot onto board
        :param bot: type of bot
        :return: None
        """
        loc_set = {0}
        items = [2, 3, bot]
        while len(loc_set) < 4:
            i = generate_random(0, self.dim - 1)
            j = generate_random(0, self.dim - 1)
            if self.layout[i][j] == 0:
                loc_set.add((i, j))
        loc_set.remove(0)
        loc_list = list(loc_set)
        while len(loc_list) > 0:
            loc_r_index = generate_random(0, len(loc_list) - 1)
            items_r_index = generate_random(0, len(items) - 1)
            tup = loc_list.pop(loc_r_index)
            item = items.pop(items_r_index)
            if item == 2:
                self.fire_loc = tup
            elif item == 3:
                self.button_loc = tup
            else:
                self.robot_loc = tup
            self.layout[tup[0]][tup[1]] = item

    def print_out(self):
        """
        Prints the layout of our ship
        :return: None
        """
        for row in self.layout:
            print(row)


def purge_half(dead_ends, layout, dim, n_purge):
    """
    Purges approximately half of all the dead ends in ship layout
    :param dead_ends: list of dead ends as tuple coordinates
    :param layout: ships layout as 2D list
    :param dim: size of list
    :param n_purge: number of dead ends we want to purge
    :return: None
    """
    for x in range(n_purge):
        r = generate_random(0, len(dead_ends) - 1)
        tup = dead_ends.pop(r)
        neighbors_blocked = []
        i = tup[0]
        j = tup[1]
        if i + 1 < dim and layout[i + 1][j] == 1:
            neighbors_blocked.append((i + 1, j))
        if i - 1 >= 0 and layout[i - 1][j] == 1:
            neighbors_blocked.append((i - 1, j))
        if j + 1 < dim and layout[i][j + 1] == 1:
            neighbors_blocked.append((i, j + 1))
        if j - 1 >= 0 and layout[i][j - 1] == 1:
            neighbors_blocked.append((i, j - 1))
        if len(neighbors_blocked) != 0:
            chosen = neighbors_blocked[generate_random(0, len(neighbors_blocked) - 1)]
            layout[chosen[0]][chosen[1]] = 0


def get_n_purge(length):
    """
    gets the number of dead ends we want to purge
    :param length: number of dead ends
    :return: half of them, rounded up to the nearest integer
    """
    if length % 2 == 0:
        return int(length / 2)
    else:
        return int(length / 2) + 1


def find_dead_ends(layout, dim):
    """
    gets the locations of every dead end cell in ship layout
    :param layout: set up of ship as 2D list
    :param dim: size of layout
    :return: set of tuple objects containing deadened locations
    """
    returned_dict = []
    for i in range(dim):
        for j in range(dim):
            if layout[i][j] == 0:
                count = 0
                if i + 1 < dim and layout[i + 1][j] == 0:
                    count += 1
                if i - 1 >= 0 and layout[i - 1][j] == 0:
                    count += 1
                if j + 1 < dim and layout[i][j + 1] == 0:
                    count += 1
                if j - 1 >= 0 and layout[i][j - 1] == 0:
                    count += 1
                if count == 1:
                    returned_dict.append((i, j))
    return returned_dict


def search_next_open(layout, blocked, dim):
    """
    def to get all the coordinate positions of blocks we can open next
    :param layout: layout of the ship
    :param blocked: set of all blocked coordinates
    :param dim: size of the layout
    :return: set of tuples that we can open next
    """
    return_set = []
    for coordinate in blocked:
        count = get_number_open_neighbors(coordinate, dim, layout)
        if count == 1:
            return_set.append(coordinate)
    return return_set


def get_number_open_neighbors(tup, dim, layout):
    """
    gets number of open neighbors
    :param dim: size of grid
    :param layout: layout of ship
    :param tup: coordinate tuple
    :return: number of neighbor open cells
    """
    count = 0
    i = tup[0]
    j = tup[1]
    indexes = [i + 1, i - 1, j + 1, j - 1]
    statics = [j, j, i, i]
    counter = 0
    for index, static in zip(indexes, statics):
        if 0 <= index < dim:
            if counter < 2:
                if layout[index][static] == 0:
                    count += 1
            else:
                if layout[static][index] == 0:
                    count += 1
        counter += 1
    return count


def generate_random(a, b):
    """
    Generates random number between a and b (inclusive)
    :param a: lower number
    :param b: higher number
    :return: random number
    """
    return random.randint(a, b)


def open_first_block(dim, layout, blocked):
    """
    unblocks the first block in the ship at random and updates the open and blocked sets
    :param dim: dimensions number
    :param layout: layout grid of ship
    :param blocked: set of blocked cells
    :return: set of open cells
    """
    r1 = generate_random(0, dim - 1)
    r2 = generate_random(0, dim - 1)
    layout[r1][r2] = 0
    blocked.remove((r1, r2))


def initialize_grid(dim):
    """
    Creates an NxN 2D list and populates it with 1's
    :param dim: dimension of grid
    :return: 2D list populated with 1's && return set of blocked cells
    """
    layout = []
    blocked_set = {0}
    for i in range(dim):
        row = []
        for j in range(dim):
            row.append(1)
            blocked_set.add((i, j))
        layout.append(row)
    blocked_set.remove(0)
    return layout, blocked_set
