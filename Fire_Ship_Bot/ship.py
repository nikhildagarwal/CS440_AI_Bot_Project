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
FIRE = 2
SAFETY_BUTTON = 3


class Ship:
    """
    Ship object
    """

    def __init__(self, dim, q, bot):
        """
        Create the ship
        :param dim: size of the ship
        :param q: flamability constant
        :param bot: which bot to place in the ship
        """
        # bot of the ship
        self.bot = bot
        # dim of the ship
        self.dim = dim
        # flamability constant of the ship
        self.q = q
        # 2d list (array) of the layout of the ship
        self.layout = []
        # generate layout with each cell initially a Wall
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(WALL)
            self.layout.append(row)
        # randomly generate a row and column index to open first
        open_i = random.randint(0, dim - 1)
        open_j = random.randint(0, dim - 1)
        # open first cell
        self.layout[open_i][open_j] = OPEN
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
        # place bot
        to_place = [bot]
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.bot_loc = (ri, rj)
        # place button
        to_place = [SAFETY_BUTTON]
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.button_loc = (ri, rj)
        # place fire
        to_place = [FIRE]
        self.fire_loc = {0}
        self.fire_loc.remove(0)
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                # store location of the start of the fire (used in bot_1)
                self.fire_start = (ri, rj)
                # store the location of the fire as a set (used in bot_2)
                self.fire_loc.add(self.fire_start)
                # store the location of the adjacent cells to the fire (used in bot_3), as well as the number of
                #   neighboring cells that are on fire (makes calculating probs very fast)
                self.fire_adj = self.get_fire_loc_adj(ri, rj)

    def get_fire_loc_adj(self, i, j):
        """
        used to INITIALLY generate the set of cells that are adjacent to the fire
        does not store cells that are WALLs because the fire can never spread to a wall cell.
        :param i: row index
        :param j: column index
        :return: Set of cells adjacent to the given cell that are NOT walls
        """
        adjs = {}
        if i + 1 < self.dim and self.layout[i + 1][j] != WALL:
            adjs[(i + 1, j)] = 1
        if i - 1 >= 0 and self.layout[i - 1][j] != WALL:
            adjs[(i - 1, j)] = 1
        if j + 1 < self.dim and self.layout[i][j + 1] != WALL:
            adjs[(i, j + 1)] = 1
        if j - 1 >= 0 and self.layout[i][j - 1] != WALL:
            adjs[(i, j - 1)] = 1
        return adjs

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
        return ""

    def spread_fire(self):
        """
        spread the fire in the ship
        :return: None
        """
        # init list of cells that need to be removed from fire_adjacent because we have opened them
        to_remove = []
        # for each cell adjacent to the fire that CAN catch on fire
        for cell in self.fire_adj:
            # calculate the probability of the current cell catching on fire
            # this will be the threshold for staying safe from the fire
            prob = 1 - pow(1 - self.q, self.fire_adj[cell])
            # randomly select a float between 0 and 0.99 inclusive
            random_float = random.uniform(0, 0.99)
            # if the randomly selected float is less than the threshold
            if random_float < prob:
                i = cell[0]
                j = cell[1]
                # current cell catches on fire
                self.layout[i][j] = FIRE
                # add cell to set of cells that are on fire
                self.fire_loc.add(cell)
                to_remove.append(cell)
        # for each cell that caught fire
        for cell in to_remove:
            # remove the cell from fire_adjacent
            del self.fire_adj[cell]
            # update set of cells that are adjacent to fire
            self.update_fire_adj(cell[0], cell[1])

    def update_fire_adj(self, i, j):
        """
        For each cell adjacent to the cell at (i, j) make sure that it is appropriately added to the fire_adjacent dict
        :param i: row index
        :param j: column index
        :return: None
        """
        # if within dimensions
        if i + 1 < self.dim:
            # if cell is already in fire_adj, add to its value
            if (i + 1, j) in self.fire_adj:
                self.fire_adj[(i + 1, j)] += 1
            # else if cell is not a wall or fire cell, add to fire_adj dict with init value 1
            elif self.layout[i + 1][j] != WALL and self.layout[i + 1][j] != FIRE:
                self.fire_adj[(i + 1, j)] = 1
        """
        repeat this for each neighbor
        """
        if i - 1 >= 0:
            if (i - 1, j) in self.fire_adj:
                self.fire_adj[(i - 1, j)] += 1
            elif self.layout[i - 1][j] != WALL and self.layout[i - 1][j] != FIRE:
                self.fire_adj[(i - 1, j)] = 1
        if j + 1 < self.dim:
            if (i, j + 1) in self.fire_adj:
                self.fire_adj[(i, j + 1)] += 1
            elif self.layout[i][j + 1] != WALL and self.layout[i][j + 1] != FIRE:
                self.fire_adj[(i, j + 1)] = 1
        if j - 1 >= 0:
            if (i, j - 1) in self.fire_adj:
                self.fire_adj[(i, j - 1)] += 1
            elif self.layout[i][j - 1] != WALL and self.layout[i][j - 1] != FIRE:
                self.fire_adj[(i, j - 1)] = 1
