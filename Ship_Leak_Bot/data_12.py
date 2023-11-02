import matplotlib.pyplot as plt

k = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
# bot 1 (1000 trials)
bot_1 = [822.757, 481.579, 333.466, 260.652, 216.405, 194.645, 187.924, 175.456, 166.381, 170.734, 174.633, 184.112,
         188.95, 196.826, 202.362, 209.054, 221.891, 218.504, 242.906, 255.375, 262.015, 267.556, 285.004, 269.298]
# bot 2A (1000 trials)
bot_2A = [678.824, 384.7, 275.705, 217.113, 205.616, 184.854, 183.379, 192.574, 202.611, 213.805, 234.327, 249.958,
          275.203, 291.806, 300.895, 315.295, 313.529, 314.102, 325.239, 314.988, 321.813, 317.6, 314.773, 302.628]
# bot 2B (1000 trials)
bot_2B = [777.277, 437.939, 314.26, 244.281, 204.419, 182.763, 170.414, 163.508, 163.515, 166.93, 172.836, 177.225,
          182.982, 188.322, 200.647, 217.813, 223.127, 231.511, 245.417, 262.06, 277.851, 289.468, 297.386, 307.263]


# bot 2C (1000 trials)


def plotter(k_arr: list[int], bot_data: list[list[float]], bot_labels: list[str], bot_colors: list[str]) -> None:
    for bot_arr, label, color in zip(bot_data, bot_labels, bot_colors):
        plt.plot(k_arr, bot_arr, color=color, marker='.', label=label)
    plt.xlim(0, 25)
    plt.xlabel('k Values')
    plt.ylabel('Average Time Spent (1000 trials per k)')
    plt.title('Time To Plug Leak vs k Value')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    plotter(k, [bot_1, bot_2A, bot_2B], ["Bot 1", "Bot 2A", "Bot 2B"], ['r','b','g'])
