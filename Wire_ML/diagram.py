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
Encoding for output classes
"""
SAFE = 0
UNSAFE = 1

"""
NumPy arrays of choices to be randomized
"""
colors = np.array([RED, BLUE, YELLOW, GREEN])
rows = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
columns = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])


class Diagram:
    def __init__(self):
        # decides where to place in a row first or column first
        decider = random.randint(0, 1)
        if decider == 0:
            encountered_yellow = False
            self.intersections = []
            self.image = []
            self.label = None
            for r in range(20):
                row = []
                for c in range(20):
                    row.append(0)
                self.image.append(row)
            # randomize selections
            np.random.shuffle(colors)
            np.random.shuffle(rows)
            np.random.shuffle(columns)
            # set labels
            for color in colors:
                if color == YELLOW:
                    encountered_yellow = True
                elif color == RED:
                    if encountered_yellow:
                        self.label = SAFE
                    else:
                        self.label = UNSAFE
            counter = 0
            # fill diagram based on randomized selections
            # places wires in rows first
            for index in range(2):
                ri = rows[index]
                ci = columns[index]
                for d in range(20):
                    if self.image[ri][d] != 0:
                        self.intersections.append((ri, d))
                    self.image[ri][d] = colors[counter]
                counter += 1
                for d in range(20):
                    if self.image[d][ci] != 0:
                        self.intersections.append((d, ci))
                    self.image[d][ci] = colors[counter]
                counter += 1
        else:
            # exact same code as above but places wires in the columns first instead of rows
            encountered_yellow = False
            self.intersections = []
            self.image = []
            self.label = None
            for r in range(20):
                row = []
                for c in range(20):
                    row.append(0)
                self.image.append(row)
            np.random.shuffle(colors)
            np.random.shuffle(rows)
            np.random.shuffle(columns)
            for color in colors:
                if color == YELLOW:
                    encountered_yellow = True
                elif color == RED:
                    if encountered_yellow:
                        self.label = SAFE
                    else:
                        self.label = UNSAFE
            counter = 0
            for index in range(2):
                ri = rows[index]
                ci = columns[index]
                for d in range(20):
                    if self.image[d][ci] != 0:
                        self.intersections.append((d, ci))
                    self.image[d][ci] = colors[counter]
                counter += 1
                for d in range(20):
                    if self.image[ri][d] != 0:
                        self.intersections.append((ri, d))
                    self.image[ri][d] = colors[counter]
                counter += 1

    def __str__(self):
        message = "label: " + str(self.label) + "\n"
        for row in self.image:
            message += str(row) + "\n"
        return message
