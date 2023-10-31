import matplotlib.pyplot as plt

k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
# bot 1 with 1000 trials
bot_1_t2 = [822.757, 481.579, 333.466, 260.652, 216.405, 194.645, 187.924, 175.456, 166.381, 170.734, 174.633, 184.112, 188.95, 196.826, 202.362, 209.054, 221.891, 218.504, 242.906, 255.375, 262.015, 267.556, 285.004, 269.298]
plt.plot(k,bot_1_t2, color='r', marker='.', label='Bot 1')
plt.xlim(0,25)
plt.xlabel('k Values')
plt.ylabel('Average Time Spent (1000 trials per k)')
plt.title('Time To Plug Leak vs k Value')
plt.legend()
plt.show()


