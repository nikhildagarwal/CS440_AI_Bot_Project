import random
import numpy as np
import heapq

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
IMPOSSIBLE = 1
POSSIBLE = 0
KNOWN = 7
LEAK = 2


def get_distance(x1, y1, x2, y2):
    return pow(pow(y2-y1,2) + pow(x2-x1,2),0.5)


class Ship:
    def __init__(self, dim, bot, k):
        """
        Create the ship
        :param dim: size of the ship
        :param bot: type of bot
        """
        self.known_loc = []
        if k > dim:
            raise ValueError("k less than or equal to dim - 4")
        self.k = k
        self.detected = False
        self.found = False
        # initialize counter to keep track of time it takes for bot to reach leak
        self.total_time = 0
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
        self.memory[open_i][open_j] = POSSIBLE
        oij_tup = (open_i,open_j)
        self.impossible_loc.remove(oij_tup)
        self.possible_loc.add(oij_tup)
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
        # print("Enter 1")
        while len(A) > 0:
            # select random cell to open among the cells that are openable
            random_index = random.randint(0, len(A) - 1)
            to_open = A.pop(random_index)
            toi = to_open[0]
            toj = to_open[1]
            # open that cell
            self.layout[toi][toj] = OPEN
            self.memory[toi][toj] = POSSIBLE
            self.impossible_loc.remove(to_open)
            self.possible_loc.add(to_open)
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
        # print("Exit 1")
        # purge half of the dead ends
        for i in range(decl):
            r_index = random.randint(0, len(dead_end_cells) - 1)
            tup = dead_end_cells.pop(r_index)
            neighbors = self.get_adj_value(tup[0], tup[1], WALL)
            if neighbors:
                n_r_index = random.randint(0, len(neighbors) - 1)
                w_tup = neighbors.pop(n_r_index)
                self.layout[w_tup[0]][w_tup[1]] = OPEN
                self.memory[w_tup[0]][w_tup[1]] = POSSIBLE
                self.impossible_loc.remove(w_tup)
                self.possible_loc.add(w_tup)
        # place bot
        to_place = [bot]
        # print("Enter 2")
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.bot_loc = (ri, rj)
                self.memory[ri][rj] = IMPOSSIBLE
                self.impossible_loc.add(self.bot_loc)
                self.possible_loc.remove(self.bot_loc)
                self.clear_box(ri, rj, k, IMPOSSIBLE)
        # print("Exit 2")
        # place leak
        # print("Enter 3")
        to_place = [LEAK]
        self.leak_loc = []
        while len(to_place) > 0:
            random_tup = random.choice(list(self.possible_loc))
            ri = random_tup[0]
            rj = random_tup[1]
            self.layout[ri][rj] = to_place.pop(0)
            # store the location of the leak as a set (used in bot_2)
            self.leak_loc.append((ri, rj))
        # print("Exit 3")

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
        print("Total time (t):",self.total_time)
        return ""

    def on_ship(self, i, j):
        """
        Returns true if given i and j coordinates are on the ship
        :param i: row index
        :param j: column index
        :return: True if on ship, False otherwise
        """
        return 0 <= i < self.dim and 0 <= j < self.dim

    def scan_box_leak(self, i, j):
        """
        Scans the current range using the bot's sensor. If the leak is detected, we mark it in memory.
        Likewise, if a leak is not detected we mark that in memory as well
        :param i: bot_loc i
        :param j: bot_loc j
        :return: None
        """
        if i-self.k <= self.leak_loc[0][0] <= i+self.k and j-self.k <= self.leak_loc[0][1] <= j+self.k:
            self.detected = True
            self.clear_box(i,j,self.k,KNOWN)
        else:
            self.clear_box(i,j,self.k,IMPOSSIBLE)
        self.total_time += 1

    def clear_box(self, i, j, k, val):
        """
        Rules out cells withing bots sensors as impossible when bot is spawned
        :param val: value to set cell too
        :param i: bot loc i
        :param j: bot loc j
        :param k: k value
        :return: None
        """
        for r in range(i-k,i+k+1):
            for c in range(j-k,j+k+1):
                if self.on_ship(r,c) and self.memory[r][c] == POSSIBLE:
                    self.memory[r][c] = val
                    rc_tup = (r,c)
                    if val == IMPOSSIBLE:
                        self.impossible_loc.add(rc_tup)
                    else:
                        self.known_loc.append(rc_tup)
                    try:
                        self.possible_loc.remove(rc_tup)
                    except KeyError:
                        pass

    def get_closest_val_in_set(self, my_set):
        heap = []
        i, j = self.bot_loc
        for tup in my_set:
            ni, nj = tup
            heapq.heappush(heap,[get_distance(i,j,ni,nj),random.randint(0,200),ni,nj])
        arr = heapq.heappop(heap)
        return arr[2],arr[3]

    def A_star(self, goal):
        searchable = []
        si, sj = self.bot_loc
        start = [0, get_distance(si,sj,goal[0],goal[1]),self.bot_loc]
        key = {self.bot_loc:start}
        heapq.heappush(searchable, start)
        visited = {0}
        visited.remove(0)
        while searchable:
            curr = heapq.heappop(searchable)
            curr_path_sum, curr_dist, curr_loc = curr
            key.pop(curr_loc)
            if curr_loc == goal:
                self.total_time += curr_path_sum
                self.layout[self.bot_loc[0]][self.bot_loc[1]] = OPEN
                self.bot_loc = curr_loc
                self.layout[self.bot_loc[0]][self.bot_loc[1]] = self.bot
                return
            visited.add(curr_loc)
            i, j = curr_loc
            nn = np.array([(i+1,j),(i-1,j),(i,j+1),(i,j-1)])
            np.random.shuffle(nn)
            for c in range(len(nn)):
                neighbor = tuple(nn[c])
                new = [curr_path_sum+1,get_distance(neighbor[0],neighbor[1],self.bot_loc[0],self.bot_loc[1]),neighbor]
                existing = key.get(neighbor,None)
                if existing is None:
                    heapq.heappush(searchable,new)
                    key[neighbor] = new
                else:
                    if existing[0] > new[0]:
                        existing[0] = new[0]
                        heapq.heapify(searchable)
        return