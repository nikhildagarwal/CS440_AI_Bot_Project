import random

"""
Final Constant vars
For visualization purposes
"""
WALL = 1
OPEN = 0
BOT_1 = -1
BOT_2 = -2
BOT_3 = -3
BOT_4 = -4
BOT_5 = -5
BOT_6 = -6
BOT_7 = -7
BOT_8 = -8
BOT_9 = -9
IMPOSSIBLE = 0
POSSIBLE = 1
UNDETECTED = 7
LEAK = 2


class Ship:
    def __init__(self, dim, bot, k):
        """
        Create the ship
        :param dim: size of the ship
        :param bot: type of bot
        """
        # initialize sets to keep track of impossible and possible cells
        self.impossible_loc = {0}
        self.impossible_loc.remove(0)
        self.possible_loc = {0}
        self.possible_loc.remove(0)
        # bot of the ship
        self.bot = bot
        # dim of the ship
        self.dim = dim
        # generate 2d list (array) of the layout of the ship
        self.layout = [[WALL for _ in range(dim)] for _ in range(dim)]
        # generate 2d list (array) ship memory of bot
        self.memory = []
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(IMPOSSIBLE)
                self.impossible_loc.add((i,j))
            self.memory.append(row)
        # randomly generate a row and column index to open first
        open_i = random.randint(0, dim - 1)
        open_j = random.randint(0, dim - 1)
        # open first cell
        self.layout[open_i][open_j] = OPEN
        self.memory[open_i][open_j] = UNDETECTED
        self.impossible_loc.remove((open_i, open_j))
        # A will keep track of all cells that are adjacent to open cells and that only have one neighbor
        A = self.get_adj_no_value(open_i, open_j)
        # F will keep track of all cells that are finalized and cannot be opened. a cell is added to this set
        #   as soon as there are two neighboring cells that are open
        F = {0}
        # keep track of all cells that are currently deadens, this list will be updated each time we open a cell
        dead_end_cells = [(open_i, open_j)]
        # open all cells while following rules (also keep track of dead end cells)
        c = 0
        # while there are still cells to open
        while len(A) > 0:
            # select random cell to open among the cells that are openable
            random_index = random.randint(0, len(A) - 1)
            to_open = A.pop(random_index)
            toi = to_open[0]
            toj = to_open[1]
            # open that cell
            self.layout[toi][toj] = OPEN
            self.memory[toi][toj] = UNDETECTED
            self.impossible_loc.remove(to_open)
            # get the neighbors of this NOW open cell
            neighbors = self.get_adj_no_value(toi, toj)
            O_count = 0
            # for each neighbor to the cell that was JUST OPENED, check if it's a wall.
            for neighbor in neighbors:
                # if it's a wall, and it is not already in the list of openable cells, and cell is not finalized,
                #   append neighbor to A
                # if it's a wall, and it is in the list of openable cells, it means that this neighbor cell
                #   to the cell that was JUST opened now has
                #   at least 2 open neighbors.
                #   Therefore, we remove this cell from the openable list and add it to the finalized list
                # if NOT A WALL, check if the cell is currently in the dead_end_cells set,
                #   since we have opened a cell next to the cell that is dead end cell, we must remove this cell,
                #   because it is NO LONGER a dead end.
                if self.layout[neighbor[0]][neighbor[1]] == WALL:
                    if neighbor not in A:
                        if neighbor not in F:
                            A.append(neighbor)
                    else:
                        A.remove(neighbor)
                        F.add(neighbor)
                else:
                    O_count += 1
                    if neighbor in dead_end_cells and c != 0:
                        dead_end_cells.remove(neighbor)
            if O_count == 1:
                dead_end_cells.append(to_open)
            c += 1
        decl = int(len(dead_end_cells) / 2)
        # purge half of the dead ends
        for i in range(decl):
            r_index = random.randint(0, len(dead_end_cells) - 1)
            tup = dead_end_cells.pop(r_index)
            neighbors = self.get_adj_value(tup[0], tup[1], WALL)
            if neighbors:
                n_r_index = random.randint(0, len(neighbors) - 1)
                w_tup = neighbors.pop(n_r_index)
                self.layout[w_tup[0]][w_tup[1]] = OPEN
                self.memory[w_tup[0]][w_tup[0]] = UNDETECTED
                self.impossible_loc.remove(w_tup)
        # place bot
        to_place = [bot]
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.bot_loc = (ri, rj)
        # place leak
        to_place = [LEAK]
        self.leak_loc = {0}
        self.leak_loc.remove(0)
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            i = self.bot_loc[0]
            j = self.bot_loc[1]
            if ((ri > i + k or ri < i - k) and (rj > j + k or rj < j - k)) and self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                # store the location of the leak as a set (used in bot_2)
                self.leak_loc.add((ri, rj))

    def get_adj_value(self, i, j, value):
        """
        get list of cells that are adjacent to the given cell and whose values equal the given value
        :param i: row index
        :param j: column index
        :param value: value to check if equal to
        :return: list of cells that contain the given value and are adjacent to the given i and j values
        """
        adjs = []
        if i + 1 < self.dim and self.layout[i + 1][j] == value:
            adjs.append((i + 1, j))
        if i - 1 >= 0 and self.layout[i - 1][j] == value:
            adjs.append((i - 1, j))
        if j + 1 < self.dim and self.layout[i][j + 1] == value:
            adjs.append((i, j + 1))
        if j - 1 >= 0 and self.layout[i][j - 1] == value:
            adjs.append((i, j - 1))
        return adjs

    def get_adj_no_value(self, i, j):
        """
        Simply return a list of adjacent cells regardless of the value of those cells
        :param i: row index
        :param j: column index
        :return: list of adjacent cells to the given i and j values
        """
        adjs = []
        if i + 1 < self.dim:
            adjs.append((i + 1, j))
        if i - 1 >= 0:
            adjs.append((i - 1, j))
        if j + 1 < self.dim:
            adjs.append((i, j + 1))
        if j - 1 >= 0:
            adjs.append((i, j - 1))
        return adjs

    def __str__(self):
        """
        Override object str function
        Visualize the ship
        :return: nothing
        """
        for row in self.layout:
            # print each row in the 2d array layout of the ship
            print(row)
        print("")
        for row in self.memory:
            # print each row in the 2d array layout of the ship
            print(row)
        return ""

    def on_ship(self, i, j):
        """
        Returns true if given i and j coordinates are on the ship
        :param i: row index
        :param j: column index
        :return: True if on ship, False otherwise
        """
        return 0 <= i < self.dim and 0 <= j < self.dim


