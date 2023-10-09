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
                if i+1 < s.dim and s.layout[i+1][j] != WALL and (i+1,j) != s.fire_start:
                    fringe.add(curr_node,Node((i+1,j)))
                if i-1 >= 0 and s.layout[i-1][j] != WALL and (i-1,j) != s.fire_start:
                    fringe.add(curr_node, Node((i - 1, j)))
                if j + 1 < s.dim and s.layout[i][j + 1] != WALL and (i,j+1) != s.fire_start:
                    fringe.add(curr_node, Node((i, j+1)))
                if j - 1 >= 0 and s.layout[i][j - 1] != WALL and (i,j - 1) != s.fire_start:
                    fringe.add(curr_node, Node((i, j - 1)))
    return bot_path


if __name__ == '__main__':
    for i in range(500):
        ship = Ship(50, 0.5, BOT_1)
        if ship.bot == BOT_1:
            path = bot_1_path(ship)
            print(i)
        elif ship.bot == BOT_2:
            pass
        elif ship.bot == BOT_3:
            pass
        else:
            pass
