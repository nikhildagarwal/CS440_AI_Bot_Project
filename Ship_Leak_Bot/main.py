from ship_12 import LEAK, WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9, Ship
from ship_12 import IMPOSSIBLE, POSSIBLE, KNOWN


def test(dim, bot, k):
    s = Ship(dim, bot, k)
    print(s)
    closest_cell = s.get_closest_val_in_set(s.possible_loc)
    print(closest_cell)
    s.A_star(closest_cell)
    print(s)


if __name__ == '__main__':
    test(5, BOT_1, 1)
