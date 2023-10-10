import matplotlib.pyplot as plt
from ship import WALL, OPEN, BOT_1, BOT_3, BOT_2, BOT_4, SAFETY_BUTTON, FIRE, Ship
from data_structure import Node, Fringe


def bot_1_path(s):
    fringe = Fringe(Node(s.bot_loc))
    bot_path = []
    while len(fringe) > 0:
        curr_node = fringe.pop()
        if curr_node.loc not in fringe.visited:
            fringe.visited.add(curr_node.loc)
            if curr_node.loc == s.button_loc:
                while curr_node.prev is not None:
                    bot_path.append(curr_node.loc)
                    curr_node = curr_node.prev
                return bot_path
            else:
                i = curr_node.loc[0]
                j = curr_node.loc[1]
                if i + 1 < s.dim and s.layout[i + 1][j] != WALL and (i + 1, j) != s.fire_start:
                    fringe.add(curr_node, Node((i + 1, j)))
                if i - 1 >= 0 and s.layout[i - 1][j] != WALL and (i - 1, j) != s.fire_start:
                    fringe.add(curr_node, Node((i - 1, j)))
                if j + 1 < s.dim and s.layout[i][j + 1] != WALL and (i, j + 1) != s.fire_start:
                    fringe.add(curr_node, Node((i, j + 1)))
                if j - 1 >= 0 and s.layout[i][j - 1] != WALL and (i, j - 1) != s.fire_start:
                    fringe.add(curr_node, Node((i, j - 1)))
    return bot_path


def bot_2_path(s):
    fringe = Fringe(Node(s.bot_loc))
    bot_path = []
    while len(fringe) > 0:
        curr_node = fringe.pop()
        if curr_node.loc not in fringe.visited:
            fringe.visited.add(curr_node.loc)
            if curr_node.loc == s.button_loc:
                while curr_node.prev is not None:
                    bot_path.append(curr_node.loc)
                    curr_node = curr_node.prev
                return bot_path
            else:
                i = curr_node.loc[0]
                j = curr_node.loc[1]
                if i + 1 < s.dim and s.layout[i + 1][j] != WALL and s.layout[i + 1][j] != FIRE:
                    fringe.add(curr_node, Node((i + 1, j)))
                if i - 1 >= 0 and s.layout[i - 1][j] != WALL and s.layout[i - 1][j] != FIRE:
                    fringe.add(curr_node, Node((i - 1, j)))
                if j + 1 < s.dim and s.layout[i][j + 1] != WALL and s.layout[i][j + 1] != FIRE:
                    fringe.add(curr_node, Node((i, j + 1)))
                if j - 1 >= 0 and s.layout[i][j - 1] != WALL and s.layout[i][j - 1] != FIRE:
                    fringe.add(curr_node, Node((i, j - 1)))
    return bot_path


def bot_3_path(s):
    fringe = Fringe(Node(s.bot_loc))
    bot_path = []
    while len(fringe) > 0:
        curr_node = fringe.pop()
        if curr_node.loc not in fringe.visited:
            fringe.visited.add(curr_node.loc)
            if curr_node.loc == s.button_loc:
                while curr_node.prev is not None:
                    bot_path.append(curr_node.loc)
                    curr_node = curr_node.prev
                return bot_path
            else:
                i = curr_node.loc[0]
                j = curr_node.loc[1]
                if (i + 1 < s.dim and s.layout[i + 1][j] != WALL and s.layout[i + 1][j] != FIRE and
                        (i+1,j) not in ship.fire_adj):
                    fringe.add(curr_node, Node((i + 1, j)))
                if (i - 1 >= 0 and s.layout[i - 1][j] != WALL and s.layout[i - 1][j] != FIRE and
                        (i-1,j) not in ship.fire_adj):
                    fringe.add(curr_node, Node((i - 1, j)))
                if (j + 1 < s.dim and s.layout[i][j + 1] != WALL and s.layout[i][j + 1] != FIRE and
                        (i,j+1) not in ship.fire_adj):
                    fringe.add(curr_node, Node((i, j + 1)))
                if (j - 1 >= 0 and s.layout[i][j - 1] != WALL and s.layout[i][j - 1] != FIRE and
                        (i,j-1) not in ship.fire_adj):
                    fringe.add(curr_node, Node((i, j - 1)))
    if len(bot_path) == 0:
        return bot_2_path(s)
    return bot_path


if __name__ == '__main__':
    q_values = []
    prob_values_bot_1 = []
    prob_values_bot_2 = []
    prob_values_bot_3 = []
    bot_list = [BOT_1, BOT_2, BOT_3]
    for i in range(101):
        if i % 2 == 0:
            q_values.append(i / 100)
    for bot in bot_list:
        for j in range(101):
            if j % 2 == 0:
                total = 0
                count = 0
                for i in range(400):
                    ship = Ship(50, j / 100, bot)
                    if ship.bot == BOT_1:
                        path = bot_1_path(ship)
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
                            path = bot_2_path(ship)
                            ship.spread_fire()
                            if len(path) == 0:
                                success = False
                                break
                            if path[-1] in ship.fire_loc:
                                success = False
                                break
                            ship.bot_loc = path.pop(-1)
                        if success:
                            count += 1
                        total += 1
                    elif ship.bot == BOT_3:
                        success = True
                        while ship.bot_loc != ship.button_loc:
                            path = bot_3_path(ship)
                            ship.spread_fire()
                            if len(path) == 0:
                                success = False
                                break
                            if path[-1] in ship.fire_loc:
                                success = False
                                break
                            ship.bot_loc = path.pop(-1)
                        if success:
                            count += 1
                        total += 1
                    else:
                        pass
                if bot == BOT_1:
                    prob_values_bot_1.append(count / total)
                elif bot == BOT_2:
                    prob_values_bot_2.append(count / total)
                elif bot == BOT_3:
                    prob_values_bot_3.append(count/total)
                print(bot,":",j/100,":",count/total)
    print(len(prob_values_bot_3))
    print(len(prob_values_bot_2))
    print(len(prob_values_bot_1))
    print(len(q_values))
    plt.plot(q_values, prob_values_bot_1, label='Bot 1', marker='o', linestyle='-', color='b')
    plt.plot(q_values, prob_values_bot_2, label='Bot 2', marker='o', linestyle='-', color='r')
    plt.plot(q_values, prob_values_bot_3, label="Bot 3", marker='o', linestyle='-', color='g')
    plt.xlabel('q values (flamability constant)')
    plt.ylabel('average probability of success (400 trials per q value)')
    plt.legend()
    plt.grid()
    plt.show()
