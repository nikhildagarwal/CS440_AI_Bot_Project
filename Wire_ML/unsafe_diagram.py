import numpy as np
import random

"""
Color Enums
"""
RED = 1
BLUE = 2
YELLOW = 3
GREEN = 4

"""
All possible ordering of wires that result in dangerous diagram
"""
orderings = [[RED, YELLOW, GREEN, BLUE],
             [RED, YELLOW, BLUE, GREEN],
             [RED, GREEN, YELLOW, BLUE],
             [RED, BLUE, YELLOW, GREEN],
             [RED, GREEN, BLUE, YELLOW],
             [RED, BLUE, GREEN, YELLOW],
             [GREEN, RED, YELLOW, BLUE],
             [BLUE, RED, YELLOW, GREEN],
             [GREEN, RED, BLUE, YELLOW],
             [BLUE, RED, GREEN, YELLOW],
             [GREEN, BLUE, RED, YELLOW],
             [BLUE, GREEN, RED, YELLOW]]
"""
order placings
"""
placings = [['r','c','r','c'],['c','r','c','r']]
rows = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
columns = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])


class UnsafeDiagram:
    def __init__(self):
        self.ans = None
        self.intersections = []
        self.image = []
        self.label = [0, 0, 0, 0] # initialize label in one-hot encoding format
        for r in range(20):
            row = []
            for c in range(20):
                row.append(0)
            self.image.append(row)
        np.random.shuffle(rows)
        np.random.shuffle(columns)
        ri = random.randint(0, len(orderings) - 1)
        order = orderings[ri]
        # set label
        if order[2] == RED:
            self.label = [1, 0, 0, 0]
            self.ans = RED
        elif order[2] == BLUE:
            self.label = [0, 1, 0, 0]
            self.ans = BLUE
        elif order[2] == YELLOW:
            self.label = [0, 0, 1, 0]
            self.ans = YELLOW
        else:
            self.label = [0, 0, 0, 1]
            self.ans = GREEN
        # randomize selections and fill diagram
        ri = random.randint(0, len(placings) - 1)
        placing = placings[ri]
        r_counter = 0
        c_counter = 0
        for p, c in zip(placing, order):
            if p == 'r':
                row = rows[r_counter]
                r_counter += 1
                for j in range(20):
                    if self.image[row][j] != 0:
                        self.intersections.append((row, j))
                    self.image[row][j] = c
            else:
                col = columns[c_counter]
                c_counter += 1
                for i in range(20):
                    if self.image[i][col] != 0:
                        self.intersections.append((i, col))
                    self.image[i][col] = c
