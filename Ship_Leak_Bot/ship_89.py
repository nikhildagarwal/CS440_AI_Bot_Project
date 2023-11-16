import random
import numpy as np
import heapq
from ship_12 import WALL, OPEN, BOT_1, BOT_2, BOT_3, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9
import math

"""
Final Constant vars
For visualization purposes
"""
IMPOSSIBLE = 0.0
POSSIBLE = 9.0
LEAK = 2


def get_distance(x1, y1, x2, y2):
    return pow(pow(y2 - y1, 2) + pow(x2 - x1, 2), 0.5)


def inbound(loc, ib, jb):
    return ib[0] <= loc[0] <= ib[1] and jb[0] <= loc[1] <= jb[1]


class Ship:
    def __init__(self, dim, bot, alpha):
        """
        Create the ship
        :param dim: size of the ship
        :param bot: type of bot
        """
        self.max_inbound = [0.0, None]
        self.max_pair = [0.0, None]
        self.detected = False
        self.alpha = alpha
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
                self.impossible_loc.add((i, j))
            self.memory.append(row)
        # randomly generate a row and column index to open first
        open_i = random.randint(0, dim - 1)
        open_j = random.randint(0, dim - 1)
        # open first cell
        self.layout[open_i][open_j] = OPEN
        self.memory[open_i][open_j] = POSSIBLE
        oij_tup = (open_i, open_j)
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
        # print("Exit 2")
        # place leaks
        # print("Enter 3")
        to_place = [LEAK, LEAK]
        self.leak_loc = []
        placed = {0}
        placed.remove(0)
        while len(to_place) > 0:
            random_tup = random.choice(list(self.possible_loc))
            if random_tup not in placed:
                placed.add(random_tup)
                ri = random_tup[0]
                rj = random_tup[1]
                self.layout[ri][rj] = to_place.pop(0)
                # store the location of the leak as a set (used in bot_2)
                self.leak_loc.append((ri, rj))
        # print("Exit 3")
        init_prob = 1 / len(self.possible_loc)
        for pi, pj in self.possible_loc:
            self.memory[pi][pj] = init_prob
        pos_list = list(self.possible_loc)
        length = len(pos_list)
        self.pairs = {}
        n = length - 1
        prob = 1 / (n * (n + 1) / 2)
        for i in range(length):
            for j in range(i + 1, length):
                cell_j = pos_list[i]
                cell_k = pos_list[j]
                self.pairs[(cell_j, cell_k)] = prob

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
        print("Total time (t):", self.total_time)
        return ""

    def on_ship(self, i, j):
        """
        Returns true if given i and j coordinates are on the ship
        :param i: row index
        :param j: column index
        :return: True if on ship, False otherwise
        """
        return 0 <= i < self.dim and 0 <= j < self.dim

    def A_start_path(self, beg, end):
        searchable = []
        ei, ej = end
        start = [0, 0, beg, None]
        heapq.heappush(searchable, start)
        visited = {0}
        visited.remove(0)
        key = {beg: start}
        while searchable:
            curr = heapq.heappop(searchable)
            curr_dist, curr_heuristic, curr_loc, prev = curr
            key.pop(curr_loc)
            if curr_loc == end:
                path = []
                head = curr
                while head[3] is not None:
                    path.insert(0, head[2])
                    head = head[3]
                return path
            visited.add(curr_loc)
            i, j = curr_loc
            neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            for neighbor in neighbors:
                ni, nj = neighbor
                if self.on_ship(ni, nj) and neighbor not in visited and self.layout[i][j] != WALL:
                    new = [curr_dist + 1, get_distance(neighbor[0], neighbor[1], ei, ej),
                           neighbor, curr]
                    existing = key.get(neighbor, None)
                    if existing is None:
                        heapq.heappush(searchable, new)
                        key[neighbor] = new
                    else:
                        if existing[0] > new[0]:
                            existing[0] = new[0]
                            existing[3] = curr
                            heapq.heapify(searchable)

    def distances_to_possible_cells(self, start):
        master = {}
        queue = [(start, 0)]
        in_queue = {start}
        visited = {0}
        visited.remove(0)
        while queue:
            curr, lvl = queue.pop(0)
            in_queue.remove(curr)
            i, j = curr
            visited.add(curr)
            if curr in self.possible_loc:
                master[curr] = lvl
            ip1 = (i + 1, j)
            im1 = (i - 1, j)
            jp1 = (i, j + 1)
            jm1 = (i, j - 1)
            if self.on_ship(i + 1, j) and ip1 not in visited and self.layout[i + 1][j] != WALL and ip1 not in in_queue:
                queue.append((ip1, lvl + 1))
                in_queue.add(ip1)
            if self.on_ship(i - 1, j) and im1 not in visited and self.layout[i - 1][j] != WALL and im1 not in in_queue:
                queue.append((im1, lvl + 1))
                in_queue.add(im1)
            if self.on_ship(i, j + 1) and jp1 not in visited and self.layout[i][j + 1] != WALL and jp1 not in in_queue:
                queue.append((jp1, lvl + 1))
                in_queue.add(jp1)
            if self.on_ship(i, j - 1) and jm1 not in visited and self.layout[i][j - 1] != WALL and jm1 not in in_queue:
                queue.append((jm1, lvl + 1))
                in_queue.add(jm1)
        return master

    def scan(self):
        self.total_time += 1
        path = self.A_start_path(self.bot_loc, self.leak_loc[0])
        d1 = len(path)
        beep_prob1 = math.exp(-1 * self.alpha * (d1 - 1))
        r1 = random.uniform(0, 0.99)
        if len(self.leak_loc) == 2:
            sp = self.A_start_path(self.bot_loc, self.leak_loc[1])
            d2 = len(sp)
            beep_prob2 = math.exp(-1 * self.alpha * (d2 - 1))
            r2 = random.uniform(0, 0.99)
            if r1 < beep_prob1 or r2 < beep_prob2:
                return True
            return False
        if r1 < beep_prob1:
            return True
        return False

    def update_all_not_found_2_leak(self, curr_loc):
        self.possible_loc.remove(curr_loc)
        self.impossible_loc.add(curr_loc)
        pairs = list(self.pairs.keys())
        pA = 0
        for pair in pairs:
            if curr_loc in pair:
                pA += self.pairs.pop(pair)
        inv = 1 - pA
        for key in self.pairs:
            self.pairs[key] /= inv

    def update_all_not_found_1_leak(self, curr_loc):
        i, j = curr_loc
        self.possible_loc.remove(curr_loc)
        self.impossible_loc.add(curr_loc)
        pA = self.memory[i][j]
        self.memory[i][j] = 0.0
        inv = 1 - pA
        for ki, kj in self.possible_loc:
            self.memory[ki][kj] /= inv

    def update_given_no_beep_2_leak(self, current):
        self.max_pair[0] = 0
        self.max_inbound[0] = 0
        self.max_inbound[1] = None
        i, j = self.bot_loc
        ib = (i - 5, i + 5)
        jb = (j - 5, j + 5)
        master = self.distances_to_possible_cells(current)
        marginal = 0
        for key in self.pairs:
            pjk = self.pairs[key]
            eq = ((1 - math.exp(-1 * self.alpha * (master[key[0]] - 1))) * (
                    1 - math.exp(-1 * self.alpha * (master[key[1]] - 1))))
            marginal += (pjk * eq)
        for key in self.pairs:
            PJK = self.pairs[key]
            EQ = ((1 - math.exp(-1 * self.alpha * (master[key[0]] - 1))) * (
                    1 - math.exp(-1 * self.alpha * (master[key[1]] - 1))))
            new_val = PJK * EQ / marginal
            self.pairs[key] = new_val
            if new_val > self.max_pair[0]:
                self.max_pair[0] = new_val
                ri = random.randint(0, 1)
                self.max_pair[1] = key[ri]
            if new_val > self.max_inbound[0] and (inbound(key[0],ib,jb) or inbound(key[1],ib,jb)):
                self.max_inbound[0] = new_val
                d1 = get_distance(i,j,key[0][0],key[0][1])
                d2 = get_distance(i,j,key[1][0],key[1][1])
                mind = min(d1,d2)
                if mind == d1:
                    self.max_inbound[1] = key[0]
                else:
                    self.max_inbound[1] = key[1]


    def update_given_no_beep_1_leak(self, current):
        self.max_pair[0] = 0
        master = self.distances_to_possible_cells(current)
        marginal_no_beep = 0
        for loc in master:
            i, j = loc
            no_beep = 1 - math.exp(-1 * self.alpha * (master[loc] - 1))
            marginal_no_beep += (self.memory[i][j] * no_beep)
        for loc in master:
            i, j = loc
            no_beep = 1 - math.exp(-1 * self.alpha * (master[loc] - 1))
            new_val = self.memory[i][j] * (no_beep / marginal_no_beep)
            self.memory[i][j] = new_val
            if new_val > self.max_pair[0]:
                self.max_pair[0] = new_val
                self.max_pair[1] = loc

    def update_given_beep_2_leak(self, current):
        self.max_pair[0] = 0
        self.max_inbound[0] = 0
        self.max_inbound[1] = None
        i, j = self.bot_loc
        ib = (i - 5, i + 5)
        jb = (j - 5, j + 5)
        master = self.distances_to_possible_cells(current)
        marginal = 0
        for key in self.pairs:
            pjk = self.pairs[key]
            eq = 1 - ((1 - math.exp(-1 * self.alpha * (master[key[0]] - 1))) * (
                    1 - math.exp(-1 * self.alpha * (master[key[1]] - 1))))
            marginal += (pjk * eq)
        for key in self.pairs:
            PJK = self.pairs[key]
            EQ = 1 - ((1 - math.exp(-1 * self.alpha * (master[key[0]] - 1))) * (
                    1 - math.exp(-1 * self.alpha * (master[key[1]] - 1))))
            new_val = PJK * EQ / marginal
            self.pairs[key] = new_val
            if new_val > self.max_pair[0]:
                self.max_pair[0] = new_val
                ri = random.randint(0, 1)
                self.max_pair[1] = key[ri]
            if new_val > self.max_inbound[0] and (inbound(key[0],ib,jb) or inbound(key[1],ib,jb)):
                self.max_inbound[0] = new_val
                d1 = get_distance(i,j,key[0][0],key[0][1])
                d2 = get_distance(i,j,key[1][0],key[1][1])
                mind = min(d1,d2)
                if mind == d1:
                    self.max_inbound[1] = key[0]
                else:
                    self.max_inbound[1] = key[1]

    def update_given_beep_1_leak(self, current):
        self.max_pair[0] = 0
        master = self.distances_to_possible_cells(current)
        marginal_yes_beep = 0
        for loc in master:
            i, j = loc
            yes_beep = math.exp(-1 * self.alpha * (master[loc] - 1))
            marginal_yes_beep += (self.memory[i][j] * yes_beep)
        for loc in master:
            i, j = loc
            yes_beep = math.exp(-1 * self.alpha * (master[loc] - 1))
            new_val = self.memory[i][j] * (yes_beep / marginal_yes_beep)
            self.memory[i][j] = new_val
            if new_val > self.max_pair[0]:
                self.max_pair[0] = new_val
                self.max_pair[1] = loc

    def get_max_loc(self):
        i, j = self.bot_loc
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        valid = []
        for neighbor in neighbors:
            ni, nj = neighbor
            if self.on_ship(ni, nj) and self.layout[ni][nj] != WALL:
                valid.append(neighbor)
        ri = random.randint(0, len(valid) - 1)
        return valid[ri]

    def get_max_loc_in_grid(self, k):
        holder = [-1, []]
        i, j = self.bot_loc
        for r in range(i - k, i + k + 1):
            for c in range(j - k, j + k + 1):
                tup = (r, c)
                if self.on_ship(r, c) and tup in self.possible_loc:
                    if self.memory[r][c] > holder[0]:
                        holder = [self.memory[r][c], [tup]]
                    elif self.memory[r][c] == holder[0]:
                        holder[1].append(tup)
        if not holder[1]:
            return None
        ri = random.randint(0, len(holder[1]) - 1)
        return holder[1][ri]

    def preprocess(self, current):
        key_list = list(self.pairs.keys())
        self.possible_loc = {0}
        self.possible_loc.remove(0)
        for key in key_list:
            if key[0] != current:
                self.possible_loc.add(key[0])
            if key[1] != current:
                self.possible_loc.add(key[1])
        prob = 1 / len(self.possible_loc)
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) in self.possible_loc:
                    self.memory[i][j] = prob
                else:
                    self.memory[i][j] = 0
