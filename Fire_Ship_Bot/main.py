import matplotlib.pyplot as plt
from ship import WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, SAFETY_BUTTON, FIRE, Ship
from data_structure import ANode
import heapq
import copy


def calculate_heuristic(i1, i2, j1, j2):
    """
    Calculates heuristic using manhattan distance between goal cell and current cell
    :param i1: current column
    :param i2: goal column
    :param j1: current row
    :param j2: goal row
    :return: float manhattan distance
    """
    return pow(pow(j2 - j1, 2) + pow(i2 - i1, 2), 0.5)


def on_board(tup, dim):
    """
    Checks if a given row and column index is within the bounds of the ship
    :param tup: cell location as a tuple (i,j)
    :param dim: dimensions of the ship Ex: n x n where n is the dimension
    :return: True if cell is on the board, false otherwise
    """
    return 0 <= tup[0] < dim and 0 <= tup[1] < dim


def fire_to_button_length(s):
    """
    Calculates the length of the shortest path from the initial start of the fire, to the safety button
    :param s: ship object
    :return: length of the short past as an integer
    """
    searchable = []
    visited = {0}
    # Create starting node
    start = ANode(s.fire_start, 1, calculate_heuristic(s.fire_start[0], s.button_loc[0], s.fire_start[1], s.button_loc[1]), None)
    # Add node to dictionary of valid nodes
    key = {s.fire_start: start}
    # push node into heap (priority queue)
    heapq.heappush(searchable, start)
    # while there are still nodes to be searched, pop the current lowest cost node and search it
    while searchable:
        current_node = heapq.heappop(searchable)
        key.pop(current_node.loc)
        # if reached goal, back track from current node and return length of valid path
        if current_node.loc == s.button_loc:
            counter = 0
            while current_node.prev is not None:
                counter += 1
                current_node = current_node.prev
            return counter
        # if not goal, add nodes location tuple to searched set (visited)
        visited.add(current_node.loc)
        i = current_node.loc[0]
        j = current_node.loc[1]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        # for each neighbor of the current cell, check if it has not been visited and not a wall
        for neighbor in neighbors:
            # if matches rules, calculate new cost and new heuristic.
            if on_board(neighbor, s.dim) and neighbor not in visited and s.layout[neighbor[0]][neighbor[1]] != WALL:
                new_g = current_node.g + 1
                new_h = calculate_heuristic(neighbor[0], s.button_loc[0], neighbor[1], s.button_loc[1])
                new_node = ANode(neighbor, new_g, new_h, current_node)
                get_node = key.get(neighbor, None)
                # if the node is found in the dictionary of nodes, update that nodes total cost, and re-heap our heap
                if get_node is not None:
                    if new_node.f < get_node.f:
                        get_node.f = new_node.f
                        get_node.g = new_node.g
                        get_node.prev = current_node
                        heapq.heapify(searchable)
                # if not found, add new node to heap
                else:
                    heapq.heappush(searchable, new_node)
                    key[neighbor] = new_node
    # returns -1 if no path found
    return -1


def bot_1_path_Astar(s):
    """
    Calculates the path from the current cell to the safety button using the rules for bot 1.
    Finds shortest path from the initial bot location to the safety button, while only avoiding the initial location of
        the fire.
    Utilizes A* algorithm for speed.
    :param s: Ship object
    :return: list of tuples (list of cells to visit in order to reach the button)
    """
    searchable = []
    visited = {0}
    # Create starting node
    start = ANode(s.bot_loc, 1, calculate_heuristic(s.bot_loc[0], s.button_loc[0], s.bot_loc[1], s.button_loc[1]), None)
    # Add node to dictionary of valid nodes
    key = {s.bot_loc: start}
    # push node into heap (priority queue)
    heapq.heappush(searchable, start)
    # while there are still nodes to be searched, pop the current lowest cost node and search it
    while searchable:
        current_node = heapq.heappop(searchable)
        key.pop(current_node.loc)
        # if reached goal, back track from current node and return path
        if current_node.loc == s.button_loc:
            r_path = []
            while current_node.prev is not None:
                r_path.append(current_node.loc)
                current_node = current_node.prev
            return r_path
        # if not goal, add nodes location tuple to searched set (visited)
        visited.add(current_node.loc)
        i = current_node.loc[0]
        j = current_node.loc[1]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        # for each neighbor of the current cell, check if it has not been visited,
        #       not a wall and not the init start of fire
        for neighbor in neighbors:
            # if matches rules for bot 1, calculate new cost and new heuristic.
            if (on_board(neighbor, s.dim) and neighbor not in visited and s.layout[neighbor[0]][neighbor[1]] != WALL
                    and neighbor != s.fire_start):
                new_g = current_node.g + 1
                new_h = calculate_heuristic(neighbor[0], s.button_loc[0], neighbor[1], s.button_loc[1])
                new_node = ANode(neighbor, new_g, new_h, current_node)
                get_node = key.get(neighbor, None)
                # if the node is found in the dictionary of nodes, update that nodes total cost, and re-heap our heap
                if get_node is not None:
                    if new_node.f < get_node.f:
                        get_node.f = new_node.f
                        get_node.g = new_node.g
                        get_node.prev = current_node
                        heapq.heapify(searchable)
                # if not found, add new node to heap
                else:
                    heapq.heappush(searchable, new_node)
                    key[neighbor] = new_node
    # returns empty path if no path is found
    return []


def bot_2_path_Astar(s):
    """
    Calculates the path from the current cell to the safety button using the rules for bot 2.
    Finds shortest path from the initial bot location to the safety button, while avoiding every cell that currently
        has a fire.
    Utilizes A* algorithm for speed.
    :param s: Ship object
    :return: list of tuples (list of cells to visit in order to reach the button)
    """
    searchable = []
    visited = {0}
    # create start Anode object
    start = ANode(s.bot_loc, 1, calculate_heuristic(s.bot_loc[0], s.button_loc[0], s.bot_loc[1], s.button_loc[1]), None)
    # add starting node to dictionary of nodes
    key = {s.bot_loc: start}
    # push starting node into heap
    heapq.heappush(searchable, start)
    # while there are still nodes to search in the heap, search them
    while searchable:
        current_node = heapq.heappop(searchable)
        key.pop(current_node.loc)
        # if we are the goal location (safety button), back track from the current node and return the path
        if current_node.loc == s.button_loc:
            r_path = []
            while current_node.prev is not None:
                r_path.append(current_node.loc)
                current_node = current_node.prev
            return r_path
        # else, add node to visited, so that we do not search it again
        visited.add(current_node.loc)
        i = current_node.loc[0]
        j = current_node.loc[1]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        # for each neighbor of the current cell, check to see if it is not a WALL and not currently on fire
        for neighbor in neighbors:
            if (on_board(neighbor, s.dim) and neighbor not in visited and s.layout[neighbor[0]][neighbor[1]] != WALL
                    and s.layout[neighbor[0]][neighbor[1]] != FIRE):
                # if rules check out, calculate cost value for the new node
                #       calculate heuristic value as well as total cost value
                new_g = current_node.g + 1
                new_h = calculate_heuristic(neighbor[0], s.button_loc[0], neighbor[1], s.button_loc[1])
                # create node
                new_node = ANode(neighbor, new_g, new_h, current_node)
                # check to see if there is currently this node in the dictionary (and therefore in the heap)
                get_node = key.get(neighbor, None)
                # if node was found, update that nodes cost values and re-heap the heap
                if get_node is not None:
                    if new_node.f < get_node.f:
                        get_node.f = new_node.f
                        get_node.g = new_node.g
                        get_node.prev = current_node
                        heapq.heapify(searchable)
                else:
                    # else, push new node to the heap, and add node to dictionary of nodes
                    heapq.heappush(searchable, new_node)
                    key[neighbor] = new_node
    # return empty path if no node is found
    return []


def bot_3_path_Astar(s):
    """
    Calculates the path from the current cell to the safety button using the rules for bot 3.
    Finds shortest path from the initial bot location to the safety button, while avoiding every cell that currently
        has a fire, and every cell currently adjacent to the fire.
    If there is no path possible avoiding cell adjacent to fire, the bot reverts to rules of bot 2.
    Utilizes A* algorithm for speed.
    :param s: Ship object
    :return: list of tuples (list of cells to visit in order to reach the button)
    """
    searchable = []
    visited = {0}
    # create starting node
    start = ANode(s.bot_loc, 1, calculate_heuristic(s.bot_loc[0], s.button_loc[0], s.bot_loc[1], s.button_loc[1]), None)
    key = {s.bot_loc: start}
    heapq.heappush(searchable, start)
    # while there are sill nodes to search in heap, search them
    while searchable:
        current_node = heapq.heappop(searchable)
        key.pop(current_node.loc)
        # if we are at the goal cell, back track rom the current node and return the path
        if current_node.loc == s.button_loc:
            r_path = []
            while current_node.prev is not None:
                r_path.append(current_node.loc)
                current_node = current_node.prev
            return r_path
        # else, add cell to visited set so that we don't search that
        visited.add(current_node.loc)
        i = current_node.loc[0]
        j = current_node.loc[1]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        # for each neighbor, check if it is not a wall, not in the fire and also not adjacent to the fire
        for neighbor in neighbors:
            if (on_board(neighbor, s.dim) and neighbor not in visited and s.layout[neighbor[0]][neighbor[1]] != WALL
                    and s.layout[neighbor[0]][neighbor[1]] != FIRE and neighbor not in s.fire_adj):
                # if the above criteria check out, calculate new costs and heuristics
                new_g = current_node.g + 1
                new_h = calculate_heuristic(neighbor[0], s.button_loc[0], neighbor[1], s.button_loc[1])
                # create new node
                new_node = ANode(neighbor, new_g, new_h, current_node)
                # if dictionary contains the node above update the cost of that node and re-heap the heap
                # (two nodes are considered equal if their location attributes are ths same)
                get_node = key.get(neighbor, None)
                if get_node is not None:
                    if new_node.f < get_node.f:
                        get_node.f = new_node.f
                        get_node.g = new_node.g
                        get_node.prev = current_node
                        heapq.heapify(searchable)
                else:
                    # else, add the new node to dictionary for look up and to the heap
                    heapq.heappush(searchable, new_node)
                    key[neighbor] = new_node
    # if there is no path based on the criteria of avoiding fire cells and fire adjacent cells,
    #       return a path based on the rules of bot 2.
    return bot_2_path_Astar(s)


# needs commenting
def bot_4_path_Astar(s):
    prob_grid = generate_probability_grid(s,1,20)
    searchable = []
    visited = {0}
    start = ANode(s.bot_loc, 0, calculate_heuristic(s.bot_loc[0], s.button_loc[0], s.bot_loc[1], s.button_loc[1]), None)
    key = {s.bot_loc: start}
    heapq.heappush(searchable, start)
    while searchable:
        current_node = heapq.heappop(searchable)
        key.pop(current_node.loc)
        if current_node.loc == s.button_loc:
            r_path = []
            while current_node.prev is not None:
                r_path.append(current_node.loc)
                current_node = current_node.prev
            return r_path
        visited.add(current_node.loc)
        i = current_node.loc[0]
        j = current_node.loc[1]
        neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        for neighbor in neighbors:
            if on_board(neighbor, s.dim):
                p_n = prob_grid[neighbor[0]][neighbor[1]]
                p_sb = prob_grid[s.button_loc[0]][s.button_loc[1]]
                cell_val = s.layout[neighbor[0]][neighbor[1]]
                if neighbor not in visited and cell_val != WALL and cell_val != FIRE and p_n <= (p_sb*2):
                    if p_n == 1:
                        p_n = 1.01
                    new_g = current_node.g + p_n + 1
                    new_h = calculate_heuristic(neighbor[0], s.button_loc[0], neighbor[1], s.button_loc[1])
                    new_node = ANode(neighbor, new_g, new_h, current_node)
                    get_node = key.get(neighbor, None)
                    if get_node is not None:
                        if new_node.f < get_node.f:
                            get_node.f = new_node.f
                            get_node.g = new_node.g
                            get_node.prev = current_node
                            heapq.heapify(searchable)
                    else:
                        heapq.heappush(searchable, new_node)
                        key[neighbor] = new_node
    return bot_2_path_Astar(s)


def generate_probability_grid(s, iterations, sim):
    """
    Generate a new grid of all zero's initially (prob_grid),
    Clone the ship 'sim' times and spread fire on each clone 'iteration' times.
    If a cell catches on fire, add 1 to the same location in 'prob_grid'.
    At the end of all simulations, loop through each cell in 'prob_grid' and divide by sim.
    This will give us a grid, where the value of each cell will be the rough probability it will be on fire,
        after x iterations
    :param s: Ship object
    :param iterations: number of time to spread_fire in each cloned ship
    :param sim: number of simulations to run (number of clones to create)
    :return: probability of fire grid
    """
    grid = [[0 for _ in range(s.dim)] for _ in range(s.dim)]
    total = sim
    for _ in range(sim):
        clone = copy.deepcopy(s)
        for _ in range(iterations):
            clone.spread_fire()
        for loc in clone.fire_loc:
            grid[loc[0]][loc[1]] += 1
    for i in range(s.dim):
        for j in range(s.dim):
            grid[i][j] /= total
    return grid


def runner(text_file, mod, trials, dim, bot_list):
    """
    Runs program
    :param text_file: text file name to save data to
    :param mod: which q values to use
    :param trials: number of trials per q value
    :param dim: dimension of ship
    :param bot_list: list of bots to simulate for
    :return: None
    """
    q_values = []
    prob_values_bot_1 = []
    prob_values_bot_2 = []
    prob_values_bot_3 = []
    prob_values_bot_4 = []
    # store q values
    for i in range(101):
        if i % mod == 0:
            q_values.append(i / 100)
    # generate values to store in file
    for bot in bot_list:
        for j in range(101):
            if j % mod == 0:
                total = 0
                count = 0
                for i in range(trials):
                    ship = Ship(dim, j / 100, bot)
                    if ship.bot == BOT_1:
                        path = bot_1_path_Astar(ship)
                        success = True
                        while path:
                            ship.spread_fire()
                            if ship.fire_loc.intersection(path):
                                success = False
                                break
                            path.pop(-1)
                        if success:
                            count += 1
                        total += 1
                    elif ship.bot == BOT_2:
                        success = True
                        while ship.bot_loc != ship.button_loc:
                            path = bot_2_path_Astar(ship)
                            if len(path) == 0:
                                success = False
                                break
                            ship.spread_fire()
                            if path[-1] in ship.fire_loc:
                                success = False
                                break
                            ship.bot_loc = path[-1]
                        if success:
                            count += 1
                        total += 1
                    elif ship.bot == BOT_3:
                        success = True
                        while ship.bot_loc != ship.button_loc:
                            path = bot_3_path_Astar(ship)
                            if len(path) == 0:
                                success = False
                                break
                            ship.spread_fire()
                            if path[-1] in ship.fire_loc:
                                success = False
                                break
                            ship.bot_loc = path[-1]
                        if success:
                            count += 1
                        total += 1
                    else:
                        success = True
                        while ship.bot_loc != ship.button_loc:
                            path = bot_4_path_Astar(ship)
                            if len(path) == 0:
                                success = False
                                break
                            ship.spread_fire()
                            if path[-1] in ship.fire_loc:
                                success = False
                                break
                            ship.bot_loc = path[-1]
                        if success:
                            count += 1
                        total += 1
                if bot == BOT_1:
                    prob_values_bot_1.append(count / total)
                elif bot == BOT_2:
                    prob_values_bot_2.append(count / total)
                elif bot == BOT_3:
                    prob_values_bot_3.append(count / total)
                elif bot == BOT_4:
                    prob_values_bot_4.append(count / total)
                print(bot, ":", j / 100, ":", count / total)
    # write data to file
    with open(text_file, 'w') as file:
        file.write("bot_1="+str(prob_values_bot_1) + "\n")
        file.write("bot_2="+str(prob_values_bot_2) + "\n")
        file.write("bot_3="+str(prob_values_bot_3) + "\n")
        file.write("bot_4="+str(prob_values_bot_4) + "\n")


if __name__ == "__main__":
    """
    RUNS PROGRAM TO GENERATE FREQUENCY OF SUCCESS VALUES
    """
    runner('test.txt',2,100,5,[BOT_1])
