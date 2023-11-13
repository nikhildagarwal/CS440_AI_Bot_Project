import math
import random


def equation(alpha, distance):
    return math.exp(-1 * alpha * (distance - 1))


def no_equation(alpha, distance):
    return 1 - math.exp(-1 * alpha * (distance - 1))


summer = 0
total = 0
alpha = 0.1
d1 = 6
d2 = 9
pl1 = equation(alpha, d1)
pl2 = equation(alpha, d2)
for _ in range(10000):
    r = random.uniform(0, 0.99)
    bl1 = False
    bl2 = False
    if r < pl1:
        bl1 = True
    if r < pl2:
        bl2 = True
    summer += (bl1 or bl2)
    total += 1
    print(summer / total)

expected = (equation(alpha,d1)*no_equation(alpha,d1) +
            equation(alpha,d2)*no_equation(alpha,d2) +
            equation(alpha,d1)*equation(alpha,d2) -
            no_equation(alpha,d1)*no_equation(alpha,d2))
print(expected)
