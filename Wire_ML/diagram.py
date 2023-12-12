import numpy as np

colors = np.array(['r', 'b', 'y', 'g'])
rows = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
columns = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])


class Diagram:
    def __init__(self):
        encountered_yellow = False
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
            if color == 'y':
                encountered_yellow = True
            elif color == 'r':
                if encountered_yellow:
                    self.label = "Safe"
                else:
                    self.label = "Unsafe"
        counter = 0
        for index in range(2):
            ri = rows[index]
            ci = columns[index]
            for d in range(20):
                self.image[ri][d] = colors[counter]
            counter += 1
            for d in range(20):
                self.image[d][ci] = colors[counter]
            counter += 1

    def __str__(self):
        message = "label: " + self.label + "\n"
        for row in self.image:
            message += str(row) + "\n"
        return message


