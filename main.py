from ship import Ship
from collections import deque

BOT_1 = -1
BOT_2 = -2
BOT_3 = -3
BOT_4 = -4
bot_set = {BOT_4, BOT_3, BOT_2, BOT_1}


def save_the_ship_bot1(grid, bot_loc):
    queue = deque()
    path = [bot_loc]
    queue.append(path)

    return True


def start_world(grid, bot, bot_loc):
    if bot == BOT_1:
        return save_the_ship_bot1(grid, bot_loc)
    elif bot == BOT_2:
        return False
    elif bot == BOT_3:
        return False
    else:
        return False


if __name__ == '__main__':
    """
    Change values here for dimension and type of bot
    """
    dimension = 5
    robot = BOT_1
    """"""
    if robot not in bot_set:
        raise TypeError("Bot must have one of the following values: -1, -2, -3, or -4")
    s1 = Ship(5)
    s1.init_environment(robot)
    s1.print_out()
    layout, robot_location = s1.layout, s1.robot_loc
    fire_suppressed = start_world(layout, robot, robot_location)
    print(fire_suppressed)
