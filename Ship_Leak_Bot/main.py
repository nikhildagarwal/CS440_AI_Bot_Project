import ship_12
import ship_34
import ship_56
import ship_789
from ship_12 import LEAK, WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, BOT_5, BOT_6, BOT_7, BOT_8, BOT_9
from ship_12 import IMPOSSIBLE, POSSIBLE, KNOWN
from data import alpha


def find_first_bot_5(s: ship_56.Ship) -> None:
    """
    Finds the first leak for bot 5 and terminates as soon as the first bot is found
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once first bot is found. The time steps are kept track with an
    attribute variable in the ship object
    """
    while not s.detected:  # while the first leak is not detected
        closest_cell = s.get_closest_val_in_set(s.possible_loc)     # choose next cell
        path = s.A_start_path(s.bot_loc, closest_cell)  # get path to next cell with A* algorithm
        s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
        for loc in path:        # for each coordinate in the path, check if that loc has the leak
            i, j = loc          # if not move to the end of the path and add the length of the path to the total time
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
    while s.known_loc:  # once the first leak is detected, check ALL the cells in the known loc set
        # we must check ALL cells since our scanner only gives a binary yes leak or no leak response, it doesn't
        # tell us if there are 2 leaks detected or 1 leak detected.
        cc = s.get_closest_val_in_set(s.known_loc)
        ci, cj = cc
        s.memory[ci][cj] = IMPOSSIBLE
        path = s.A_start_path(s.bot_loc,cc)     # get path to the closest cell where the leak may be located
        s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
        s.total_time += len(path)
        s.bot_loc = path[-1]
        s.known_loc.remove(cc)
        if s.bot_loc in s.leak_loc:
            s.leak_loc.remove(s.bot_loc)
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
    s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot


def find_second_bot_5(s: ship_56.Ship) -> None:
    """
    Finds the second leak for bot 5 and terminates as soon as the first bot is found
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once first bot is found. The time steps are kept track with an
    attribute variable in the ship object
    """
    s.detected = False
    while not s.detected:   # loops until leak is detected or leak is found by moving into a cell
        cc = s.get_closest_val_in_set(s.possible_loc)   # get the closest cell where leak could be possible
        path = s.A_start_path(s.bot_loc,cc)     # A* to find path to that cell
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
    s.found = False
    s.known_loc.remove(s.bot_loc)
    while not s.found:  # once leak is detected, search cells in the detected space until leak is found
        # since this function will only be entered given that only once cell was found, once we find a leak
        # we can automatically terminate this loop and exit the function
        cc = s.get_closest_val_in_set(s.known_loc)
        path = s.A_start_path(s.bot_loc,cc)
        s.total_time += len(path)
        s.bot_loc = path[-1]
        if s.bot_loc in s.leak_loc:
            return
        s.known_loc.remove(s.bot_loc)


def find_first_bot_6A(s: ship_56.Ship) -> None:
    """
    Finds the first leak in bot 6A (first implementation of bot 6)
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once a leak is found
    """
    while not s.detected:   # loops until leak is detected
        closest_cell = s.next_cell_bot2A()      # Chooses next cell like bot 2A
        path = s.A_start_path(s.bot_loc, closest_cell)  # gets path using A*
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
    while s.known_loc:  # searches ALL cells where leak was detected in order to make sure that it does
        # not miss out on the second leak
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


def find_second_bot_6A(s: ship_56.Ship) -> None:
    """
    Finds the second leak in bot 6A (first implementation of bot 6)
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once a leak is found
    """
    s.detected = False
    while not s.detected:   # loops until second leak is detected or leak is found by entering a cell
        cc = s.next_cell_bot2A()    # chooses cell like bot 2A
        path = s.A_start_path(s.bot_loc, cc)    # gets path with A* algorithm
        for loc in path:
            s.total_time += 1
            if loc in s.leak_loc:
                return
            try:
                s.possible_loc.remove(loc)
            except KeyError:
                pass
        s.bot_loc = path[-1]
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
    s.found = False
    s.known_loc.remove(s.bot_loc)
    while not s.found:  # searches set of cells where leak was detected until second leaks is found, then terminates
        cc = s.get_closest_val_in_set(s.known_loc)
        path = s.A_start_path(s.bot_loc, cc)
        s.total_time += len(path)
        s.bot_loc = path[-1]
        if s.bot_loc in s.leak_loc:
            return
        s.known_loc.remove(s.bot_loc)


def find_first_bot_6B(s: ship_56.Ship) -> None:
    """
    Finds the first leak in bot 6B (second implementation of bot 6)
    Exact same code as find_first_bot_6A EXCEPT for the way it chooses the next cell in the first while loop.
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once a leak is found
    """
    while not s.detected:
        closest_cell = s.next_cell_bot2B()  # ONLY CHANGE - chooses next cell like bot 2B
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


def find_second_bot_6B(s: ship_56.Ship) -> None:
    """
    Finds the first leak in bot 6B (second implementation of bot 6)
    Exact same code as find_first_bot_6A EXCEPT for the way it chooses the next cell in the first while loop.
    :param s: a ship_56 object which is unique to the 2 leak deterministic situation
    :return: None - terminates once a leak is found
    """
    s.detected = False
    while not s.detected:
        cc = s.next_cell_bot2B()    # ONLY CHANGE - chooses next cell like bot 2B
        path = s.A_start_path(s.bot_loc, cc)
        for loc in path:
            s.total_time += 1
            if loc in s.leak_loc:
                return
            try:
                s.possible_loc.remove(loc)
            except KeyError:
                pass
        s.bot_loc = path[-1]
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
    s.found = False
    s.known_loc.remove(s.bot_loc)
    while not s.found:
        cc = s.get_closest_val_in_set(s.known_loc)
        path = s.A_start_path(s.bot_loc, cc)
        s.total_time += len(path)
        s.bot_loc = path[-1]
        if s.bot_loc in s.leak_loc:
            return
        s.known_loc.remove(s.bot_loc)


def test_bot1(dim: int, k: int) -> float:
    """
    Generates test environment for bot 1, and runes the experiment. When a leak is found, this function returns the
    total amount of time has elapsed (number of moves the bot has taken)
    :param dim: dimension of the ship
    :param k: k value (size of sensor)
    :return: total elapsed time (number of moves)
    """
    s = ship_12.Ship(dim, BOT_1, k)
    while not s.detected:   # loops until first leak is detected
        closest_cell = s.get_closest_val_in_set(s.possible_loc)     # chooses the closest cell (euclidian distance)
        s.A_star(closest_cell)  # moves to that cell using A* algorithm
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.scan_box_leak(s.bot_loc[0], s.bot_loc[1])
    if s.bot_loc == s.leak_loc[0]:
        return s.total_time
    s.known_loc.remove(s.bot_loc)
    s.memory[s.bot_loc[0]][s.bot_loc[1]] = IMPOSSIBLE
    while not s.found:  # this loop is only entered if the leak is detected
        # loops until the leak is found
        closest_cell = s.get_closest_val_in_set(s.known_loc)
        s.A_star(closest_cell)
        if s.bot_loc == s.leak_loc[0]:
            return s.total_time
        s.known_loc.remove(s.bot_loc)
        s.memory[s.bot_loc[0]][s.bot_loc[1]] = IMPOSSIBLE


def test_bot2A(dim: int, k: int) -> float:
    """
    Generates test environment for the first implementation of bot 2
    ONLY difference from bot 1 is how it chooses the next cell
    :param dim: dimension of the ship
    :param k: size of sensor
    :return: the total time elapsed (number of moves taken)
    """
    s = ship_12.Ship(dim, BOT_2, k)
    while not s.detected:
        closest_cell = s.next_cell_bot2A()  # ONLY CHANGE - choose next cell using different logic from bot 1
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
    """
    Generates test environment for the first second of bot 2
    ONLY difference from bot 1 is how it chooses the next cell
    :param dim: dimension of the ship
    :param k: size of sensor
    :return: the total time elapsed (number of moves taken)
    """
    s = ship_12.Ship(dim, BOT_2, k)
    while not s.detected:
        closest_cell = s.next_cell_bot2B()  # ONLY CHANGE - choose next cell using bot 2B logic
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
    """
    Generates test environment for the FINAL VERSION of bot 2
    :param dim: dimension of the ship
    :param k: size of sensor
    :return: the total time elapsed (number of moves taken)
    """
    # for k values less than 7, bot 2 using bot 2A logic
    # otherwise it uses bot 2B logic
    if k <= 6:
        return test_bot2A(dim, k)
    return test_bot2B(dim, k)


def test_bot3(dim: int, a: float) -> float:
    """
    Generates test environment for bot 3
    :param dim: size of ship
    :param a: sensitivity of sensor
    :return: time elapsed to find leak (number of moves)
    """
    s = ship_34.Ship(dim, BOT_3, a)     # initialize ship
    s.max_pair[1] = s.get_max_loc()     # gets the cell that currently has the largest probability of success
    while not s.found:  # loops until the leak is found
        next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)    # gets the path to the cell with the
        # highest probability using an A* algorithm
        for loc in path_to_next_cell:
            # checks each cell along the path to see if a cell contains the leak
            # updates probabilities along the path as well
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc == s.leak_loc[0]:
                return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        # once the bot has moved to the next cell, it will use its sensor
        beeped = s.scan()
        # if it receives a beep it updates the probability accordingly
        # it not it also updates the probability accordingly
        if beeped:
            s.update_given_beep(s.bot_loc)
        else:
            s.update_given_no_beep(s.bot_loc)


def test_bot4(dim: int, a: float) -> float:
    """
    Generates test environment for bot 4
    Has the exact same implementation as bot 3 EXCEPT for how it chooses the next cell
    Makes use of a form of local search, which confines it search for the cell with max probability
    to the immediate 11x11 grid around the current cell
    :param dim: size of board
    :param a: sensitivity of sensor
    :return: total elapsed time (number of moves the bot takes)
    """
    s = ship_34.Ship(dim, BOT_3, a)     # init ship
    s.max_pair[1] = s.get_max_loc()     # get the first cell that the bot will travel too
    while not s.found:  # loops until the leak is found
        next_cell = s.get_max_loc_in_grid(5)    # gets the cell with the maximum probability within its
        # immediate 11x11 grid. If however there are no cells with a probability greater than 0, the bot
        # will REVERT to finding the cell with the max probability anywhere on the ship (same as bot 3)
        if next_cell is None:
            next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)    # get path to next cell via A* algorithm
        for loc in path_to_next_cell:
            # same as bot 3 (checks every cell along path)
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc == s.leak_loc[0]:
                return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        beeped = s.scan()
        # same as bot 3 for updating probabilities based on receiving a beep or not
        if beeped:
            s.update_given_beep(s.bot_loc)
        else:
            s.update_given_no_beep(s.bot_loc)


def test_bot5(dim: int, k: int) -> float:
    """
    Generates test environment for bot 5
    :param dim: size of ship
    :param k: size of scanner
    :return: total time elapsed (number of moves the bot makes)
    """
    s = ship_56.Ship(dim, BOT_5, k)
    find_first_bot_5(s)     # find the first leak using the functions defined above in this file
    if not s.leak_loc:      # checks to see if ONLY ONE LEAK WAS FOUND (not both)
        return s.total_time
    find_second_bot_5(s)    # find the second leak
    return s.total_time


def test_bot6A(dim: int, k: int) -> float:
    """
    Generates test environment for bot 6A
    :param dim: size of ship
    :param k: size of scanner
    :return: total time elapsed (number of moves the bot makes)
    """
    # Same as test_bot5 but with different function calls for this bot
    s = ship_56.Ship(dim, BOT_6, k)
    find_first_bot_6A(s)    # bot 6A function call
    if not s.leak_loc:
        return s.total_time
    find_second_bot_6A(s)   # bot 6A function call
    return s.total_time


def test_bot6B(dim: int, k: int) -> float:
    """
    Generates test environment for bot 6B
    :param dim: size of ship
    :param k: size of scanner
    :return: total time elapsed (number of moves the bot makes)
    """
    # Same as test_bot5 except for the function calls to find the first and second leaks
    s = ship_56.Ship(dim, BOT_6, k)
    find_first_bot_6B(s)        # function call for 6B
    if not s.leak_loc:
        return s.total_time
    find_second_bot_6B(s)       # function call for 6B
    return s.total_time


def test_bot6C(dim: int, k: int) -> float:
    """
    Generates test environment for the FINAL VERSION of bot 6
    :param dim: size of ship
    :param k: size of scanner
    :return: total time elapsed (total number of moves)
    """
    # if k is less than 5, use bot 6A logic
    if k < 5:
        return test_bot6A(dim, k)
    # otherwise use bot 6B logic
    return test_bot6B(dim, k)


def test_bot7(dim: int, a: float) -> float:
    """
    Generates test environment for bot 7
    :param dim: size of ship
    :param a: sensitivity of sensor
    :return: total time elapsed (total number of moves)
    """
    s = ship_789.Ship(dim, BOT_7, a)
    s.max_pair[1] = s.get_max_loc()
    while s.leak_loc:   # proceeds like bot 3 until BOTH leaks are found
        # updates probabilities exactly like bot 3
        next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)
        for loc in path_to_next_cell:
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc in s.leak_loc:
                # if a leak is found, it removes the leak from the set of leak locations
                s.leak_loc.remove(s.bot_loc)
                if len(s.leak_loc) == 0:
                    # if the set of leak locations is 0, meaning both have been found (terminate the loop)
                    return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        beeped = s.scan()
        if beeped:
            s.update_given_beep_7(s.bot_loc)
        else:
            s.update_given_no_beep_7(s.bot_loc)


def test_bot8(dim: int, a: float) -> float:
    """
    Generates test environment for bot 8
    :param dim: size of ship
    :param a: sensitivity of sensor
    :return: total time elapsed (total number of moves)
    """
    # EXACT same implementation as bot 7 except for how it updates the probabilities
    s = ship_789.Ship(dim, BOT_8, a)
    s.max_pair[1] = s.get_max_loc()
    while s.leak_loc:   # loops until both leaks are found
        next_cell = s.max_pair[1]
        path_to_next_cell = s.A_start_path(s.bot_loc, next_cell)
        for loc in path_to_next_cell:
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = OPEN
            s.bot_loc = loc
            s.layout[s.bot_loc[0]][s.bot_loc[1]] = s.bot
            s.total_time += 1
            if s.bot_loc in s.leak_loc:
                s.leak_loc.remove(s.bot_loc)
                if len(s.leak_loc) == 0:
                    return s.total_time
            if s.bot_loc in s.possible_loc:
                s.update_all_not_found(s.bot_loc)
        beeped = s.scan()
        if beeped:
            s.update_given_beep_8(s.bot_loc)    # different probability update call function
        else:
            s.update_given_no_beep_8(s.bot_loc)     # different probability update call function


def k_tester(trial_count, bot):
    """
    Test function to facilitate experimentation for bots with parameter k
    :param trial_count: number of trials per k value
    :param bot: type of bot
    :return: None - simply prints the array to console
    """
    output = []
    for k in range(1, 25):  # k values from 1 to 24 (largest range for 50x50 ship)
        t = 0
        ts = 0
        for i in range(trial_count):  # trials per k value
            t += 1
            if bot == BOT_1:
                ts += test_bot1(50, k)
            elif bot == BOT_2:
                ts += test_bot2C(50, k)  # change test function to test different versions of bot 2
            elif bot == BOT_5:
                ts += test_bot5(50,k)
            elif bot == BOT_6:
                ts += test_bot6C(50, k)
            if i % 50 == 0:
                print("k:", k, "i:", i, " time:", ts / t)
        output.append(ts / t)
    print(output)


def alpha_tester(trial_count, bot):
    """
    Test function to facilitate experimentation for bots with parameter a
    :param trial_count: number of trials per k value
    :param bot: type of bot
    :return: None - Simply output the array to the console
    """
    output = []
    for a in alpha:     # see the list of alpha values in data.py
        t = 0
        ts = 0
        for i in range(trial_count):
            t += 1
            if bot == BOT_3:
                ts += test_bot3(50, a)
            elif bot == BOT_4:
                ts += test_bot4(50, a)
            elif bot == BOT_7:
                ts += test_bot7(50, a)
            elif bot == BOT_8:
                ts += test_bot8(50, a)
            if i % 50 == 0:
                print("a:", a, "i:", i, " time:", ts / t)
        output.append(ts / t)
    print(output)


if __name__ == '__main__':
    """
    To test for a specific bot simply call the k_tester function or alpha tester function
    Ex: k_tester(200, BOT_5)    # 200 trials per k value for tested on bot 5
    ** NOTE ** The size of all ships are preset to 50x50
    """
    alpha_tester(400, BOT_8)

