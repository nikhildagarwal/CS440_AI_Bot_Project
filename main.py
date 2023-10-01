from ship import Ship
from collections import deque
from data_structure import Fringe
from data_structure import Node

BOT_1 = -1
BOT_2 = -2
BOT_3 = -3
BOT_4 = -4
SAFETY_BUTTON = 3
FIRE = 2
bot_set = {BOT_4, BOT_3, BOT_2, BOT_1}


def after_check_steps(i, j, curr_node,fringe):
    """
    Add node to fringe if fringe has not visited that node before
    :param i: index i
    :param j: index j
    :param curr_node: Node that we have searched next
    :param fringe: fringe data structure
    :return: None
    """
    new_tup = (i, j)
    if new_tup not in fringe.visited:
        fringe.add(Node(new_tup), curr_node, new_tup)


def save_the_ship_bot1_fringe(grid, bot_loc):
    """
    Runs bfs algorithm on bot 1.
    Generates shortest path to safety button, only avoiding the initial cell where the first started
    :param grid: layout of ship with bot, safety button and fire all placed
    :param bot_loc: initial location tuple of the bot
    :return: True if bot reaches the location of the safety button, False otherwise
    """
    fringe = Fringe(bot_loc)
    fire_start = s1.fire_loc[0]
    sol_path = []
    dim = s1.dim
    while not fringe.queue.is_empty():
        curr_node = fringe.pop()
        if curr_node.loc == s1.button_loc:
            while curr_node.prev is not None:
                sol_path.append(curr_node.loc)
                curr_node = curr_node.prev
            break
        i = curr_node.loc[0]
        j = curr_node.loc[1]
        if i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) != fire_start:
            after_check_steps(i + 1, j, curr_node, fringe)
        if i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) != fire_start:
            after_check_steps(i - 1, j, curr_node, fringe)
        if j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) != fire_start:
            after_check_steps(i, j + 1, curr_node, fringe)
        if j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) != fire_start:
            after_check_steps(i, j - 1, curr_node, fringe)
    if len(sol_path) == 0:
        print("No safe path available")
        return False
    sol_path.reverse()
    for t in range(len(sol_path)):
        s1.spread_fire()
        if sol_path[t] in s1.fire_loc:
            print("T: " + str(t+1))
            print(sol_path)
            grid[sol_path[t][0]][sol_path[t][1]] = "X"
            s1.print_out()
            print("Fire engulfed Bot")
            return False
        else:
            grid[sol_path[t][0]][sol_path[t][1]] = BOT_1
            grid[s1.robot_loc[0]][s1.robot_loc[1]] = 0
            s1.robot_loc = sol_path[t]
        print("T: " + str(t + 1))
        print(sol_path)
        s1.print_out()
    grid[sol_path[-1][0]][sol_path[-1][1]] = "W"
    s1.print_out()
    return True


def save_the_ship_bot2_fringe(grid):
    """
    Runs the bfs algorithm for bot 2.
    The bfs algorithm calculates the shortest path to the safety button, avoiding all cells which are currently on fire.
    After each time the bot moves, it re-calculates the shortest path
    to the safety button while avoiding all cells currently on fire
    :param grid: layout of the ship with button, bot, and fire all placed
    :return: True if bot reaches safety button, False otherwise
    """
    dim = s1.dim
    signal = True
    while signal:
        bot_loc = s1.robot_loc
        if bot_loc in s1.fire_loc:
            grid[bot_loc[0]][bot_loc[1]] = "X"
            s1.print_out()
            print("Fire engulfed bot")
            return False
        if bot_loc == s1.button_loc:
            return True
        fringe = Fringe(bot_loc)
        sol_path = []
        t = 1
        while not fringe.queue.is_empty():
            curr_node = fringe.pop()
            if curr_node.loc == s1.button_loc:
                while curr_node.prev is not None:
                    sol_path.append(curr_node.loc)
                    curr_node = curr_node.prev
                break
            i = curr_node.loc[0]
            j = curr_node.loc[1]
            if i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) not in s1.fire_loc:
                after_check_steps(i+1,j,curr_node,fringe)
            if i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) not in s1.fire_loc:
                after_check_steps(i-1,j,curr_node,fringe)
            if j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) not in s1.fire_loc:
                after_check_steps(i,j+1,curr_node,fringe)
            if j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) not in s1.fire_loc:
                after_check_steps(i,j-1,curr_node,fringe)
        if len(sol_path) == 0:
            print("No safe path to the button")
            return False
        print("T: " + str(t))
        t += 1
        print(sol_path)
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = 0
        s1.robot_loc = sol_path[-1]
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = BOT_2
        if s1.robot_loc == s1.button_loc:
            grid[s1.robot_loc[0]][s1.robot_loc[1]] = "W"
            s1.print_out()
            return True
        s1.spread_fire()
        s1.print_out()


def save_the_ship_bot3_fringe(grid):
    dim = s1.dim
    signal = True
    while signal:
        bot_loc = s1.robot_loc
        if bot_loc in s1.fire_loc:
            grid[bot_loc[0]][bot_loc[1]] = "X"
            s1.print_out()
            print("Fire engulfed bot")
            return False
        if bot_loc == s1.button_loc:
            return True
        fringe = Fringe(bot_loc)
        sol_path = []
        t = 1
        while not fringe.queue.is_empty():
            curr_node = fringe.pop()
            if curr_node.loc == s1.button_loc:
                while curr_node.prev is not None:
                    sol_path.append(curr_node.loc)
                    curr_node = curr_node.prev
                break
            i = curr_node.loc[0]
            j = curr_node.loc[1]
            if (i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) not in s1.fire_loc and (i + 1, j)
                    not in s1.fire_neighbors):
                after_check_steps(i + 1, j, curr_node, fringe)
            if (i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) not in s1.fire_loc and (i - 1, j)
                    not in s1.fire_neighbors):
                after_check_steps(i - 1, j, curr_node, fringe)
            if (j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) not in s1.fire_loc and (i, j + 1)
                    not in s1.fire_neighbors):
                after_check_steps(i, j + 1, curr_node, fringe)
            if (j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) not in s1.fire_loc and (i, j-1)
                    not in s1.fire_neighbors):
                after_check_steps(i, j - 1, curr_node, fringe)
        if len(sol_path) == 0:
            fringe1 = Fringe(bot_loc)
            while not fringe1.queue.is_empty():
                curr_node = fringe1.pop()
                if curr_node.loc == s1.button_loc:
                    while curr_node.prev is not None:
                        sol_path.append(curr_node.loc)
                        curr_node = curr_node.prev
                    break
                i = curr_node.loc[0]
                j = curr_node.loc[1]
                if i + 1 < dim and grid[i + 1][j] != 1 and (i + 1, j) not in s1.fire_loc:
                    after_check_steps(i + 1, j, curr_node, fringe1)
                if i - 1 >= 0 and grid[i - 1][j] != 1 and (i - 1, j) not in s1.fire_loc:
                    after_check_steps(i - 1, j, curr_node, fringe1)
                if j + 1 < dim and grid[i][j + 1] != 1 and (i, j + 1) not in s1.fire_loc:
                    after_check_steps(i, j + 1, curr_node, fringe1)
                if j - 1 >= 0 and grid[i][j - 1] != 1 and (i, j - 1) not in s1.fire_loc:
                    after_check_steps(i, j - 1, curr_node, fringe1)
            if len(sol_path) == 0:
                print("No safe path to the button")
                return False
        print("T: " + str(t))
        t += 1
        print(sol_path)
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = 0
        s1.robot_loc = sol_path[-1]
        grid[s1.robot_loc[0]][s1.robot_loc[1]] = BOT_3
        if s1.robot_loc == s1.button_loc:
            grid[s1.robot_loc[0]][s1.robot_loc[1]] = "W"
            s1.print_out()
            return True
        s1.spread_fire()
        s1.print_out()


def start_world(grid, bot, bot_loc):
    """
    Routes the job to a different algorithm based on the type of robot
    :param grid: ship layout
    :param bot: type of bot
    :param bot_loc: starting location of bot as a tuple
    :return: Boolean value of whether the robot was able to save the ship
    """
    if bot == BOT_1:
        return save_the_ship_bot1_fringe(grid, bot_loc)
    elif bot == BOT_2:
        return save_the_ship_bot2_fringe(grid)
    elif bot == BOT_3:
        return save_the_ship_bot3_fringe(grid)
    else:
        return False


if __name__ == '__main__':
    """
    Change values here for dimension and type of bot
    """
    dimension = 50
    bot = BOT_3
    q = 0.7
    """"""
    if bot not in bot_set:
        raise TypeError("Bot must have one of the following values: -1, -2, -3, or -4")
    if q <= 0 or q >= 1:
        raise TypeError("q must be between 0 and 1")
    if dimension <= 1:
        raise TypeError("Dimension of the ship layout must be at least 2 x 2")
    s1 = Ship(dimension, q)
    s1.init_environment(bot)
    print("T: 0")
    s1.print_out()
    layout, robot_location = s1.layout, s1.robot_loc
    fire_suppressed = start_world(layout, bot, robot_location)
    print("Fire Suppressed: " + str(fire_suppressed))
