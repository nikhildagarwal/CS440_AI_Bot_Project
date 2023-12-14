import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# sample counts for testing
sample_counts = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000, 40000, 50000, 60000, 75000, 100000]
# learning rates for testing
learning_rates = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]

# performance of binary classifier neural network
performance = [0.499516, 0.500118, 0.49983, 0.50072, 0.49978, 0.499266, 0.499838, 0.500572, 0.500326, 0.5006, 0.498648,
               0.499986, 0.498926, 0.499792, 0.499622, 0.50124, 0.499492, 0.499926, 0.500326, 0.50016, 0.49969,
               0.499024, 0.500336, 0.501024, 0.500278, 0.500118, 0.499932, 0.498854, 0.499352, 0.500382, 0.500232,
               0.499516, 0.500376, 0.500166, 0.509434, 0.69517, 0.558988, 0.701592, 0.774744, 0.772684, 0.499236,
               0.500474, 0.499808, 0.501268, 0.716144, 0.796358, 0.802196, 0.745638, 0.808554, 0.79202, 0.500696,
               0.499056, 0.602376, 0.6089, 0.745702, 0.781942, 0.792748, 0.815274, 0.81417, 0.816328, 0.498882,
               0.614234, 0.72021, 0.739702, 0.756254, 0.803614, 0.789328, 0.796218, 0.795516, 0.834166, 0.499712,
               0.745828, 0.81252, 0.7857, 0.76698, 0.776634, 0.806416, 0.886614, 0.8077, 0.901042, 0.498824, 0.740314,
               0.813144, 0.808226, 0.815404, 0.875672, 0.83249, 0.80614, 0.929862, 0.795178, 0.736636, 0.79568,
               0.748964, 0.788184, 0.910162, 0.9679, 0.960242, 0.985744, 0.858214, 0.987416, 0.780028, 0.798, 0.852216,
               0.797324, 0.969924, 0.966306, 0.84613, 0.985464, 0.982528, 0.857486, 0.816216, 0.80586, 0.865118,
               0.937492, 0.989252, 0.989776, 0.827466, 0.979028, 0.992162, 0.994694, 0.788476, 0.825838, 0.925282,
               0.979318, 0.988602, 0.990634, 0.994066, 0.99303, 0.983934, 0.988372, 0.798668, 0.916474, 0.983902,
               0.991436, 0.992188, 0.995526, 0.988934, 0.997316, 0.996222, 0.997498]
# samples sizes that were used to calculate accuracy of binary-classifier
x_vals = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
          2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000,
          5000, 5000, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 10000, 10000, 10000, 10000, 10000,
          10000, 10000, 10000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000,
          20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 25000, 25000, 25000, 25000, 25000,
          25000, 25000, 25000, 25000, 25000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000,
          50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 60000, 60000, 60000, 60000, 60000,
          60000, 60000, 60000, 60000, 60000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000,
          100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]

"""
* Takes the above binary-classification data and sifts through the values that were generated with a learning 
rate of 0.01
* Plots the data with a line plot
"""
max_perf = []
max_x = []
c = 0
for p, x in zip(performance, x_vals):
    if c % 10 == 9:
        max_perf.append(p)
        max_x.append(x)
    c += 1
plt.plot(max_x, max_perf, marker='o', markersize=4)
plt.xticks(max_x, [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000, 40000, 50000, 60000, 75000, 100000])
plt.title("Accuracy of Model with learning rate of 0.1")
plt.xlabel("Training Dataset Sample Count")
plt.ylabel("Accuracy of Model on Test Dataset (500,000 samples)")
plt.xticks(rotation=90)
plt.show()

"""
plots the above binary-classification data on a 2D plot
"""
plt.plot(x_vals, performance, marker='o', markersize=4, linestyle='none')
plt.xticks(x_vals,
           [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
            1000, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 5000, 5000, 5000, 5000, 5000, 5000, 5000,
            5000, 5000, 5000, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 10000, 10000, 10000, 10000,
            10000, 10000, 10000, 10000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000,
            15000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 25000, 25000, 25000, 25000,
            25000, 25000, 25000, 25000, 25000, 25000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000,
            40000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 60000, 60000, 60000, 60000,
            60000, 60000, 60000, 60000, 60000, 60000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000,
            75000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000])
plt.xticks(rotation=90)
plt.title("Accuracy of Model Based On Learning Rates from [0.001, 0.01] and Various Training Sample Sizes")
plt.xlabel("Training Dataset Sample Count")
plt.ylabel("Accuracy of Model on Test Dataset (500,000 samples)")
plt.show()


"""
Plots the above binary classification data on a 3D plot which allows for the visualization of how 
sample size and learning rate combine to effect the accuracy of the model on test data.
"""
x = x_vals
y = learning_rates * 14
z = performance
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r', marker='o')
for (i, j, k) in zip(x, y, z):
    ax.plot([i, i], [j, j], [k-0.1, k], color='gray')
ax.set_xlabel('Training Sample Size')
ax.set_ylabel('Learning Rate')
ax.set_zlabel('Accuracy of Model in Training Set (500,000 samples)')
plt.show()


performance_mc = [0.333162, 0.334136, 0.332452, 0.33324, 0.332946, 0.333546, 0.333504, 0.333196, 0.332884, 0.250298,
                  0.333438, 0.332922, 0.334476, 0.33252, 0.333158, 0.333296, 0.332678, 0.250314, 0.249504, 0.334294,
                  0.33402, 0.333738, 0.3323, 0.332538, 0.333342, 0.332946, 0.332602, 0.33356, 0.332824, 0.33498,
                  0.333524, 0.331946, 0.33329, 0.33304, 0.333896, 0.333194, 0.332568, 0.332614, 0.333452, 0.517672,
                  0.333946, 0.334458, 0.332396, 0.332976, 0.532398, 0.512728, 0.499328, 0.49944, 0.80479, 0.635444,
                  0.333806, 0.333722, 0.333584, 0.335434, 0.6054, 0.893736, 0.576244, 0.789638, 0.974264, 0.927148,
                  0.334252, 0.33331, 0.65283, 0.922212, 0.798838, 0.969262, 0.97681, 0.977298, 0.971168, 0.98351,
                  0.333654, 0.350406, 0.79884, 0.950146, 0.966852, 0.979116, 0.977148, 0.984786, 0.984632, 0.986592,
                  0.333302, 0.813286, 0.961424, 0.939628, 0.976596, 0.986344, 0.99182, 0.991424, 0.990854, 0.994386,
                  0.356946, 0.97406, 0.981986, 0.99167, 0.991398, 0.995144, 0.995674, 0.996658, 0.9979, 0.994584,
                  0.801834, 0.976982, 0.989524, 0.992476, 0.994484, 0.997754, 0.997716, 0.998642, 0.998704, 0.998552,
                  0.945778, 0.98144, 0.993808, 0.9951, 0.997092, 0.998334, 0.998954, 0.997688, 0.999412, 0.998154,
                  0.96994, 0.992872, 0.994412, 0.995578, 0.998302, 0.998754, 0.999104, 0.999298, 0.999384, 0.99945,
                  0.9775, 0.993102, 0.997406, 0.998712, 0.999228, 0.999312, 0.99933, 0.99962, 0.999226, 0.999382]
x_vals_mc = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
             1000, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 5000, 5000, 5000, 5000, 5000, 5000,
             5000, 5000, 5000, 5000, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 10000, 10000, 10000,
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000,
             15000, 15000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 25000, 25000, 25000,
             25000, 25000, 25000, 25000, 25000, 25000, 25000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000,
             40000, 40000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 60000, 60000, 60000,
             60000, 60000, 60000, 60000, 60000, 60000, 60000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000,
             75000, 75000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]
"""
plots the above binary-classification data on a 2D plot
"""
plt.plot(x_vals_mc, performance_mc, marker='o', markersize=4, linestyle='none')
plt.xticks(x_vals,
           [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,
            1000, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 5000, 5000, 5000, 5000, 5000, 5000, 5000,
            5000, 5000, 5000, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 7500, 10000, 10000, 10000, 10000,
            10000, 10000, 10000, 10000, 10000, 10000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000,
            15000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 20000, 25000, 25000, 25000, 25000,
            25000, 25000, 25000, 25000, 25000, 25000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000, 40000,
            40000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 50000, 60000, 60000, 60000, 60000,
            60000, 60000, 60000, 60000, 60000, 60000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000, 75000,
            75000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000])
plt.xticks(rotation=90)
plt.title("Accuracy of Model Based On Learning Rates from [0.001, 0.01] and Various Training Sample Sizes")
plt.xlabel("Training Dataset Sample Count")
plt.ylabel("Accuracy of Model on Test Dataset (500,000 samples)")
plt.show()

"""
Plots the above binary classification data on a 3D plot which allows for the visualization of how 
sample size and learning rate combine to effect the accuracy of the model on test data.
"""
x = x_vals_mc
y = learning_rates * 14
z = performance_mc
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r', marker='o')
for (i, j, k) in zip(x, y, z):
    ax.plot([i, i], [j, j], [k-0.1, k], color='gray')
ax.set_xlabel('Training Sample Size')
ax.set_ylabel('Learning Rate')
ax.set_zlabel('Accuracy of Model in Training Set (500,000 samples)')
plt.show()


"""
* Takes the above binary-classification data and sifts through the values that were generated with a learning 
rate of 0.01
* Plots the data with a line plot
"""
max_perf = []
max_x = []
c = 0
for p, x in zip(performance_mc, x_vals_mc):
    if c % 10 == 9:
        max_perf.append(p)
        max_x.append(x)
    c += 1
plt.plot(max_x, max_perf, marker='o', markersize=4)
plt.xticks(max_x, [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000, 40000, 50000, 60000, 75000, 100000])
plt.title("Accuracy of Model with learning rate of 0.1")
plt.xlabel("Training Dataset Sample Count")
plt.ylabel("Accuracy of Model on Test Dataset (500,000 samples)")
plt.xticks(rotation=90)
plt.show()