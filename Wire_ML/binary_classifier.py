from generate_data import Generate
import numpy as np
import random
from diagram import SAFE, UNSAFE
import matplotlib.pyplot as plt
from data import sample_counts, learning_rates


def extract_data(image, ic):
    r, c = ic
    ans = [image[r][c]]
    neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1), (r + 1, c + 1),
                 (r - 1, c - 1), (r + 1, c - 1), (r - 1, c + 1)]
    for n in neighbors:
        nr, nc = n
        if 0 <= nr <= 19 and 0 <= nc <= 19:
            ans.append(image[nr][nc])
        else:
            ans.append(0)
    return ans


def train_model(filename1, filename2, sample_count, learning_rate):
    data = Generate(sample_count)
    weights1 = []
    for i in range(10):
        row = []
        for _ in range(36):
            row.append(random.uniform(0, 0.005))
        weights1.append(row)
    weights1 = np.asmatrix(weights1)
    weights2 = []
    for i in range(2):
        row = []
        for _ in range(10):
            row.append(random.uniform(0, 0.001))
        weights2.append(row)
    weights2 = np.asmatrix(weights2)
    mse = []
    for image, label, inter_coordinates in zip(data.images, data.labels, data.intersections):
        start = []
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        if label == SAFE:
            target = [1, 0]
        else:
            target = [0, 1]
        target = np.asmatrix(target)
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        loss = out2 - target
        mse.append(list(np.asarray(loss)[0]))
        to_sub = np.dot(loss.T, out1)
        weights2 -= learning_rate * to_sub
        front = np.dot(loss, weights2)
        tout1 = np.asarray(out1)
        temp = tout1 * (1 - tout1)
        tf1 = np.asarray(front)
        diff = tf1 * temp
        diff = np.asmatrix(diff)
        weights1 -= learning_rate * np.dot(diff.T, start)
    np.savetxt(filename1, weights1, delimiter=',')
    np.savetxt(filename2, weights2, delimiter=',')
    return mse


def test_model(filename1, filename2, sample_count):
    data = Generate(sample_count)
    weights1 = np.loadtxt(filename1, delimiter=",")
    weights2 = np.loadtxt(filename2, delimiter=",")
    correct = 0
    total = 0
    for image, label, inter_coordinates in zip(data.images, data.labels, data.intersections):
        start = []
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        out2 = np.asarray(out2)
        if out2[0][0] > out2[0][1]:
            if label == SAFE:
                correct += 1
        else:
            if label == UNSAFE:
                correct += 1
        total += 1
    return correct / total


performance = []
x_vals = []
for sc in sample_counts:
    for lr in learning_rates:
        train_model("bm1.csv", "bm2.csv", sc, lr)
        accuracy = test_model("bm1.csv", "bm2.csv", 500000)
        print(sc, ":", lr, ":", accuracy)
        performance.append(accuracy)
        x_vals.append(sc)
print("performance =", performance)
print("x_vals =", x_vals)

mse_array = train_model("bm1.csv", "bm2.csv", 5000, 0.01)
mse = []
summer = 0
total = 0
for x1, x2 in mse_array:
    summer += ((x1 ** 2) + (x2 ** 2)) / 2
    total += 1
    mse.append(summer / total)
plt.plot(list(range(1, 5001)), mse)
plt.xlabel("i-th sample (5000 samples, 0.01 learning rate)")
plt.ylabel("Average MSE")
plt.title("Average Mean Squared Error Up to the i-th element (MSE)")
plt.show()
