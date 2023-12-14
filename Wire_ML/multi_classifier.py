from generate_data import GenerateUnsafe
import numpy as np
import random
from diagram import RED, BLUE, YELLOW, GREEN
import matplotlib.pyplot as plt
from data import sample_counts, learning_rates


def extract_data(image, ic):
    """
    Extracts the data in the surrounding 3x3 square with an intersection of two wires centered in the box.
    :param image: image matrix (2D array)
    :param ic: tuple (coordinate) of the intersection
    :return: an array of 11 integer values representing the values around and in the intersection.
        as well as the maximum color that is present in that box and the number of times this color is seen.
    """
    r, c = ic
    ans = [image[r][c]]
    neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1), (r + 1, c + 1),
                 (r - 1, c - 1), (r + 1, c - 1), (r - 1, c + 1)]
    holder = {1: 0, 2: 0, 3: 0, 4: 0}
    for n in neighbors:
        nr, nc = n
        if 0 <= nr <= 19 and 0 <= nc <= 19:
            ans.append(image[nr][nc])  # scan box and append to output array
            if image[nr][nc] != 0:
                holder[image[nr][nc]] += 1
        else:
            ans.append(0)
    max_val = [None, 0]
    # find max val in frequency dictionary in place
    for key in holder:
        if max_val[0] is None:
            max_val[0] = key
            max_val[1] = holder[key]
        else:
            if holder[key] > max_val[1]:
                max_val[1] = holder[key]
                max_val[0] = key
    ans.append(max_val[0])
    ans.append(max_val[1])
    return ans


def train_model(filename1, filename2, sample_count, learning_rate):
    """
    Trains a 3 layer neural network.
    Has input layer, 1 hidden layer, and output layer.
    :param filename1: first CSV file to store weights 1
    :param filename2: second CSV file to store weights 2
    :param sample_count: The number of samples that we want to training the model with
    :param learning_rate: learning rate of the network (how much the loss of
            one sample can effect the weights of the model)
    :return: MSE Loss vector Array
    """
    data = GenerateUnsafe(sample_count)  # generate n samples
    weights1 = []
    for i in range(18):
        row = []
        for _ in range(44):
            row.append(random.uniform(0, 0.005))  # init weights
        weights1.append(row)
    weights1 = np.asmatrix(weights1)
    weights2 = []
    for i in range(4):
        row = []
        for _ in range(18):
            row.append(random.uniform(0, 0.005))  # init weights
        weights2.append(row)
    weights2 = np.asmatrix(weights2)
    mse = []
    for image, label, inter_coordinates in zip(data.images, data.labels, data.intersection_list):
        start = []
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        target = np.asmatrix(label)
        """
        forward propagation step
        """
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        """
        loss calculation step
        """
        loss = out2 - target
        mse.append(list(np.asarray(loss)[0]))
        """
        back propagation step
        """
        to_sub = np.dot(loss.T, out1)
        weights2 -= learning_rate * to_sub
        front = np.dot(loss, weights2)
        tout1 = np.asarray(out1)
        temp = tout1 * (1 - tout1)
        tf1 = np.asarray(front)
        diff = tf1 * temp
        diff = np.asmatrix(diff)
        weights1 -= learning_rate * np.dot(diff.T, start)
    # save weights in CSV
    np.savetxt(filename1, weights1, delimiter=',')
    np.savetxt(filename2, weights2, delimiter=',')
    return mse


def test_model(filename1, filename2, sample_count):
    data = GenerateUnsafe(sample_count)
    # load preexisting weights into the weight matrices
    weights1 = np.loadtxt(filename1, delimiter=",")
    weights2 = np.loadtxt(filename2, delimiter=",")
    correct = 0
    total = 0
    for image, label, inter_coordinates, a in zip(data.images, data.labels, data.intersection_list, data.answer):
        start = []
        # extract input vector
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        """
        forward propagate the data
        """
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        out2 = np.asarray(out2)
        out2 = list(out2[0])
        """
        compare data and check for accuracy
        """
        s = [(out2[0], RED), (out2[1], BLUE), (out2[2], YELLOW), (out2[3], GREEN)]
        s.sort(key=lambda x: x[0])
        local_ans = s[3][1]
        if local_ans == a:
            correct += 1
        total += 1
    return correct / total


"""
Graphs the Average Mean Squared Error (MSE) over time of the model to show learning
"""
mse_array = train_model("mm1.csv", "mm2.csv", 5000, 0.01)
mse = []
summer = 0
total = 0
for x1, x2, x3, x4 in mse_array:
    summer += ((x1 ** 2) + (x2 ** 2) + (x3 ** 2) + (x4 ** 2)) / 4
    total += 1
    mse.append(summer / total)
plt.plot(list(range(1, 5001)), mse)
plt.xlabel("i-th sample (5000 samples, 0.01 learning rate)")
plt.ylabel("Average MSE")
plt.title("Average Mean Squared Error Up to the i-th element (MSE of Multi-Classifier)")
plt.show()


"""
Evaluates the accuracy of different models with varying sample sizes and learning rates.
"""
performance = []
x_vals = []
for sc in sample_counts:
    for lr in learning_rates:
        train_model("mm1.csv", "mm2.csv", sc, lr)
        accuracy = test_model("mm1.csv", "mm2.csv", 500000)
        print(sc, ":", lr, ":", accuracy)
        performance.append(accuracy)
        x_vals.append(sc)
print("performance_mc =", performance)
print("x_vals_mc =", x_vals)
