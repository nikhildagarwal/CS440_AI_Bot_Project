from ship_12 import LEAK, WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9, Ship
from ship_12 import IMPOSSIBLE, POSSIBLE, KNOWN


def test(dim, bot, k):
    s = Ship(dim, bot, k)
    while not s.detected:
        closest_cell = s.get_closest_val_in_set(s.possible_loc)
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.scan_box_leak(s.bot_loc[0],s.bot_loc[1])
    if s.bot_loc == s.leak_loc[0]:
        return s.total_time
    s.known_loc.remove(s.bot_loc)
    s.memory[s.bot_loc[0]][s.bot_loc[1]] = IMPOSSIBLE
    while not s.found:
        closest_cell = s.get_closest_val_in_set(s.known_loc)
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.known_loc.remove(s.bot_loc)
        s.memory[s.bot_loc[0]][s.bot_loc[1]] = IMPOSSIBLE
    return 0


if __name__ == '__main__':
    total = 0
    t_sum = 0
    ans = []
    for k in range(1,25):
        for i in range(1000):
            yo = test(50, BOT_1, k)
            t_sum += yo
            total += 1
            if i % 10 == 0:
                print("k =",k,"i =",i," ",t_sum/total)
        ans.append(t_sum / total)
    print(ans)
