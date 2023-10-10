import matplotlib.pyplot as plt

bot_1 = [1.0, 0.965, 0.9675, 0.92, 0.915, 0.865, 0.86, 0.835, 0.81, 0.7925, 0.7275,
         0.7125, 0.7175, 0.6775, 0.7025, 0.6425, 0.6225, 0.6125, 0.6025, 0.5975, 0.57, 0.5975,
         0.4925, 0.51, 0.4625, 0.4975]

bot_2=[1.0
,0.975
,0.9625
,0.9175
,0.9175
,0.895
,0.8675
,0.8075
,0.785
,0.7725
,0.78
,0.7475
,0.7225
,0.725
,0.6675
,0.64
,0.605
,0.6125
,0.63
,0.58
,0.555
,0.5525
,0.505
,0.5075
,0.4425
,0.5025]

q_values = []
for j in range(101):
    if j % 4 == 0:
        q_values.append(j/100)

plt.plot(q_values, bot_1, label='Bot 1', marker='o', linestyle='-', color='b')
plt.plot(q_values, bot_2, label='Bot 2', marker='o', linestyle='-', color='r')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid()
plt.show()
