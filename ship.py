import random
import copy

WALL = 1
OPEN = 0
BOT_1 = -1
BOT_2 = -2
BOT_3 = -3
BOT_4 = -4
FIRE = 2
SAFETY_BUTTON = 3


class Ship:
    def __init__(self, dim, q, bot):
        self.bot = bot
        self.dim = dim
        self.q = q
        self.layout = []
        # generate all 1's
        for i in range(dim):
            row = []
            for j in range(dim):
                row.append(WALL)
            self.layout.append(row)
        open_i = random.randint(0, dim - 1)
        open_j = random.randint(0, dim - 1)
        # open first cell
        self.layout[open_i][open_j] = OPEN
        A = self.get_adj_no_value(open_i, open_j)
        F = {0}
        dead_end_cells = [(open_i, open_j)]
        # open all cells while following rules (also keep track of dead end cells)
        c = 0
        while len(A) > 0:
            random_index = random.randint(0, len(A) - 1)
            to_open = A.pop(random_index)
            toi = to_open[0]
            toj = to_open[1]
            self.layout[toi][toj] = OPEN
            neighbors = self.get_adj_no_value(toi, toj)
            O_count = 0
            for neighbor in neighbors:
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
        # purge half dead ends
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
                self.bot_loc = (ri,rj)
        # place button
        to_place = [SAFETY_BUTTON]
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.button_loc = (ri,rj)
        # place fire
        to_place = [FIRE]
        self.fire_loc = {0}
        self.fire_loc.remove(0)
        while len(to_place) > 0:
            ri = random.randint(0, dim - 1)
            rj = random.randint(0, dim - 1)
            if self.layout[ri][rj] == OPEN:
                self.layout[ri][rj] = to_place.pop(0)
                self.fire_start = (ri, rj)
                self.fire_loc.add(self.fire_start)
                self.fire_adj = self.get_fire_loc_adj(ri,rj)

    def get_fire_loc_adj(self,i,j):
        adjs = {}
        if i + 1 < self.dim and self.layout[i+1][j] != WALL:
            adjs[(i + 1, j)] = 1
        if i - 1 >= 0 and self.layout[i-1][j] != WALL:
            adjs[(i - 1, j)] = 1
        if j + 1 < self.dim and self.layout[i][j+1] != WALL:
            adjs[(i, j + 1)] = 1
        if j - 1 >= 0 and self.layout[i][j-1] != WALL:
            adjs[(i, j - 1)] = 1
        return adjs

    def get_adj_value(self, i, j, value):
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
        for row in self.layout:
            print(row)
        return ""

    def spread_fire(self):
        to_remove = []
        for cell in self.fire_adj:
            prob = 1 - pow(1-self.q,self.fire_adj[cell])
            random_float = random.uniform(0, 0.99)
            if random_float < prob:
                i = cell[0]
                j = cell[1]
                self.layout[i][j] = FIRE
                self.fire_loc.add(cell)
                to_remove.append(cell)
        for cell in to_remove:
            del self.fire_adj[cell]
            self.update_fire_adj(cell[0],cell[1])

    def update_fire_adj(self,i,j):
        if i + 1 < self.dim:
            if (i+1,j) in self.fire_adj:
                self.fire_adj[(i+1,j)] += 1
            elif self.layout[i+1][j] != WALL and self.layout[i+1][j] != FIRE:
                self.fire_adj[(i+1,j)] = 1
        if i - 1 >= 0:
            if (i-1,j) in self.fire_adj:
                self.fire_adj[(i-1,j)] += 1
            elif self.layout[i-1][j] != WALL and self.layout[i-1][j] != FIRE:
                self.fire_adj[(i-1,j)] = 1
        if j + 1 < self.dim:
            if (i,j+1) in self.fire_adj:
                self.fire_adj[(i,j+1)] += 1
            elif self.layout[i][j+1] != WALL and self.layout[i][j+1] != FIRE:
                self.fire_adj[(i,j+1)] = 1
        if j - 1 >= 0:
            if (i,j-1) in self.fire_adj:
                self.fire_adj[(i,j-1)] += 1
            elif self.layout[i][j-1] != WALL and self.layout[i][j-1] != FIRE:
                self.fire_adj[(i,j-1)] = 1


