import ship_12
import ship_34
from ship_12 import LEAK, WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9
from ship_12 import IMPOSSIBLE, POSSIBLE, KNOWN


def test_bot1(dim: int, k: int) -> float:
    s = ship_12.Ship(dim, BOT_1, k)
    while not s.detected:
        closest_cell = s.get_closest_val_in_set(s.possible_loc)
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
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
    return s.total_time


def test_bot2A(dim: int, k: int) -> float:
    s = ship_12.Ship(dim, BOT_2, k)
    while not s.detected:
        closest_cell = s.next_cell_bot2A()
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
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


def test_bot2B(dim: int, k: int) -> float:
    s = ship_12.Ship(dim, BOT_2, k)
    while not s.detected:
        closest_cell = s.next_cell_bot2B()
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
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


def test_bot2C(dim: int, k: int) -> float:
    if k < 5:
        return test_bot2A(dim,k)
    return test_bot2B(dim,k)


def test_bot3(dim: int, alpha: float) -> float:
    s = ship_34.Ship(dim, BOT_3, alpha)
    print(s)
    while not s.found:
        next_cell = s.next_cell_bot3(s.possible_loc)
        if s.A_star_stop_along_path(next_cell):
            return s.total_time
        if s.bot_loc == s.leak_loc[0]:
            s.found = True
            print(s)
            return s.total_time
        s.update_prob_not_found()
        print(s)
        beeped = s.sense(s.A_star(s.leak_loc[0],False))
        if beeped:
            s.update_scanned_yes_beep()
        else:
            s.update_scanned_no_beep()
        print(s)


def k_tester(trial_count, bot):
    output = []
    for k in range(1, 25):                          # k values from 1 to 24 (largest range for 50x50 ship)
        t = 0
        ts = 0
        for i in range(trial_count):                # 1000 trials per k value
            t += 1
            if bot == BOT_1:
                ts += test_bot1(50, k)
            elif bot == BOT_2:
                ts += test_bot2C(50,k)          # change test function to test different versions of bot 2
            if i % 50 == 0:
                print("k:", k, "i:", i, " prob:", ts / t)
        output.append(ts / t)
    print(output)


if __name__ == '__main__':
    a = test_bot3(25,0.5)




