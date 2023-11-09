import ship_12
import ship_34
import ship_56
from ship_12 import LEAK, WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9
from ship_12 import IMPOSSIBLE, POSSIBLE, KNOWN
from data import alpha


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
        return test_bot2A(dim, k)
    return test_bot2B(dim, k)


def test_bot3(dim: int, a: float) -> float:
    s = ship_34.Ship(dim, BOT_3, a)
    s.max_pair[1] = s.get_max_loc()
    while not s.found:
        next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)
        for loc in path_to_next_cell:
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc == s.leak_loc[0]:
                return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        beeped = s.scan()
        if beeped:
            s.update_given_beep(s.bot_loc)
        else:
            s.update_given_no_beep(s.bot_loc)


def test_bot4(dim: int, a: float) -> float:
    s = ship_34.Ship(dim, BOT_3, a)
    s.max_pair[1] = s.get_max_loc()
    while not s.found:
        next_cell = s.get_max_loc_in_grid(8)
        if next_cell is None:
            next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)
        for loc in path_to_next_cell:
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc == s.leak_loc[0]:
                return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        beeped = s.scan()
        if beeped:
            s.update_given_beep(s.bot_loc)
        else:
            s.update_given_no_beep(s.bot_loc)


def find_first_bot(s: ship_56.Ship) -> None:
    while not s.detected:
        closest_cell = s.get_closest_val_in_set(s.possible_loc)
        path = s.A_start_path(s.bot_loc, closest_cell)
        s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
        for loc in path:
            i, j = loc
            s.memory[i][j] = IMPOSSIBLE
            try:
                s.possible_loc.remove(loc)
            except KeyError:
                pass

            s.total_time += 1
            if loc in s.leak_loc:
                s.leak_loc.remove(loc)
                s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
                return
        s.bot_loc = path[-1]
        s.scan_box_leak(s.bot_loc[0],s.bot_loc[1])
    s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
    while s.known_loc:
        cc = s.get_closest_val_in_set(s.known_loc)
        ci, cj = cc
        s.memory[ci][cj] = IMPOSSIBLE
        path = s.A_start_path(s.bot_loc,cc)
        s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
        s.total_time += len(path)
        s.bot_loc = path[-1]
        s.known_loc.remove(cc)
        if s.bot_loc in s.leak_loc:
            s.leak_loc.remove(s.bot_loc)
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
    s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot


def find_second_bot(s: ship_56.Ship) -> None:
    s.detected = False
    while not s.detected:
        cc = s.get_closest_val_in_set(s.possible_loc)
        path = s.A_start_path(s.bot_loc,cc)
        for loc in path:
            s.total_time += 1
            if loc in s.leak_loc:
                return
            try:
                s.possible_loc.remove(loc)
            except KeyError:
                pass
        s.bot_loc = path[-1]
        s.scan_box_leak(s.bot_loc[0],s.bot_loc[1])
    print(s)


def test_bot5(dim: int, k: int) -> float:
    s = ship_56.Ship(dim, BOT_5, k)
    print(s)
    find_first_bot(s)
    print(s)
    print(s.possible_loc)
    print(s.bot_loc)
    print(s.leak_loc)
    if not s.leak_loc:
        return s.total_time
    find_second_bot(s)


def k_tester(trial_count, bot):
    output = []
    for k in range(1, 25):  # k values from 1 to 24 (largest range for 50x50 ship)
        t = 0
        ts = 0
        for i in range(trial_count):  # 1000 trials per k value
            t += 1
            if bot == BOT_1:
                ts += test_bot1(50, k)
            elif bot == BOT_2:
                ts += test_bot2C(50, k)  # change test function to test different versions of bot 2
            if i % 50 == 0:
                print("k:", k, "i:", i, " time:", ts / t)
        output.append(ts / t)
    print(output)


def alpha_tester(trial_count, bot):
    output = []
    for a in alpha:
        t = 0
        ts = 0
        for i in range(trial_count):
            t += 1
            if bot == BOT_3:
                ts += test_bot4(50, a)  # change test function for bot
            if i % 50 == 0:
                print("a:", a, "i:", i, " time:", ts / t)
        output.append(ts / t)
    print(output)


if __name__ == '__main__':
    for i in range(1):
        print(test_bot5(5,1))
