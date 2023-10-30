import matplotlib.pyplot as plt

k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
# bot 1 with 1000 trials
bot_1_t2 = [819.34, 646.708, 541.266, 473.965, 424.648, 387.325, 357.951, 334.861, 316.565, 302.391, 291.078, 281.964, 274.471, 268.773, 264.693, 261.171, 258.528, 256.935, 255.942, 255.724, 255.780, 256.976, 257.771, 258.602]
plt.plot(k,bot_1_t2, color='r', marker='.', label='Bot 1')
plt.xlim(0,25)
plt.xlabel('k Values')
plt.ylabel('Average Time Spent (1000 trials per k)')
plt.title('Time To Plug Leak vs k Value')
plt.legend()
plt.show()

