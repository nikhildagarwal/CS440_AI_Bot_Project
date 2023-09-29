from ship import Ship
from collections import deque

BOT_1 = -1
BOT_2 = -2
BOT_3 = -3
BOT_4 = -4
SAFETY_BUTTON = 3
FIRE = 2
bot_set = {BOT_4, BOT_3, BOT_2, BOT_1}


def clone_and_queue(li, q, tup):
    """
    helper method to clone list and append it to queue for bfs algorithm
    :param li: list to clone
    :param q: queue to append cloned list
    :param tup: coordinate tup to append to cloned list
    :return: None
    """
    cloned = list(li)
    cloned.append(tup)
    q.append(cloned)


def save_the_ship_bot1(grid, bot_loc):
    dim = len(grid)
    queue = deque()
    path = [bot_loc]
    queue.append(path)
    sol_path = None
    fire_start = s1.fire_loc[0]
    while len(queue) > 0:
        curr_path = queue.popleft()
        loc = curr_path[-1]
        i = loc[0]
        j = loc[1]
        if grid[i][j] == SAFETY_BUTTON:
            sol_path = curr_path
            break
        if i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) != fire_start and (i+1, j) not in curr_path:
            clone_and_queue(curr_path, queue, (i + 1, j))
        if i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) != fire_start and (i-1, j) not in curr_path:
            clone_and_queue(curr_path, queue, (i - 1, j))
        if j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) != fire_start and (i, j+1) not in curr_path:
            clone_and_queue(curr_path, queue, (i, j + 1))
        if j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) != fire_start and (i, j-1) not in curr_path:
            clone_and_queue(curr_path, queue, (i, j - 1))
    if sol_path is None:
        return False
    sol_path.pop(0)
    for t in range(len(sol_path)):
        s1.spread_fire()
        if sol_path[t] in s1.fire_loc:
            s1.print_out()
            print(" ")
            return False
        else:
            grid[sol_path[t][0]][sol_path[t][1]] = BOT_1
        s1.print_out()
        print(" ")
    return True


def save_the_ship_bot2(grid):
    dim = s1.dim
    signal = True
    while signal:
        bot_loc = s1.robot_loc
        if bot_loc in s1.fire_loc:
            return False
        if bot_loc == s1.button_loc:
            return True
        queue = deque()
        p = [bot_loc]
        queue.append(p)
        sol_path = None
        while len(queue) > 0:
            path = queue.popleft()
            curr_loc = path[-1]
            i = curr_loc[0]
            j = curr_loc[1]
            if grid[i][j] == SAFETY_BUTTON:
                sol_path = path
                break
            if i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) not in s1.fire_loc and (i+1, j) not in path:
                clone_and_queue(path, queue, (i + 1, j))
            if i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) not in s1.fire_loc and (i-1, j) not in path:
                clone_and_queue(path, queue, (i - 1, j))
            if j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) not in s1.fire_loc and (i, j+1) not in path:
                clone_and_queue(path, queue, (i, j + 1))
            if j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) not in s1.fire_loc and (i, j-1) not in path:
                clone_and_queue(path, queue, (i, j - 1))
        if sol_path is None:
            return False
        sol_path.pop(0)
        print(sol_path)
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = 0
        s1.robot_loc = sol_path[0]
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = BOT_2
        s1.spread_fire()
        s1.print_out()
        print("")


def start_world(grid, bot, bot_loc):
    if bot == BOT_1:
        return save_the_ship_bot1(grid, bot_loc)
    elif bot == BOT_2:
        return save_the_ship_bot2(grid)
    elif bot == BOT_3:
        return False
    else:
        return False


if __name__ == '__main__':
    """
    Change values here for dimension and type of bot
    """
    dimension = 5
    bot = BOT_2
    q = 0.9
    """"""
    if bot not in bot_set:
        raise TypeError("Bot must have one of the following values: -1, -2, -3, or -4")
    s1 = Ship(dimension, q)
    s1.init_environment(bot)
    s1.print_out()
    print(" ")
    layout, robot_location = s1.layout, s1.robot_loc
    fire_suppressed = start_world(layout, bot, robot_location)
    print(fire_suppressed)
