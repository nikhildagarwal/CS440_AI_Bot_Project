from generate_data import Generate
import numpy as np
import random
from diagram import SAFE, UNSAFE
import matplotlib.pyplot as plt
from data import sample_counts, learning_rates


def extract_data(image, ic):
    """
    Extracts the data in the surrounding 3x3 square with an intersection of two wires centered in the box.
    :param image: image matrix (2D array)
    :param ic: tuple (coordinate) of the intersection
    :return: an array of 9 integer values representing the values around and in the intersection.
    """
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
    """
    Trains a 3 layer neural network.
    Has input layer, 1 hidden layer, and output layer.
    :param filename1: first CSV file to store weights 1
    :param filename2: second CSV file to store weights 2
    :param sample_count: The number of samples that we want to training the model with
    :param learning_rate: learning rate of the network (how much the loss of
            one sample can effect the weights of the model)
    :return: MSE loss vector array
    """
    data = Generate(sample_count) # generate n samples to train the model on
    weights1 = []
    for i in range(10):
        row = []
        for _ in range(36):
            row.append(random.uniform(0, 0.005))  # init weights as random floats from 0 to 0.005
        weights1.append(row)
    weights1 = np.asmatrix(weights1)
    weights2 = []
    for i in range(2):
        row = []
        for _ in range(10):
            row.append(random.uniform(0, 0.005))  # init weights as random floats from 0 to 0.005
        weights2.append(row)
    weights2 = np.asmatrix(weights2)
    mse = []  # array to store loss vectors which we later return to calculate MSE
    for image, label, inter_coordinates in zip(data.images, data.labels, data.intersections):
        start = []
        # generate input vector (extracting the intersection values)
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        # set labels
        if label == SAFE:
            target = [1, 0]
        else:
            target = [0, 1]
        """
        forward propagation step
        """
        target = np.asmatrix(target)
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        """
        loss vector calculation step
        """
        loss = out2 - target
        mse.append(list(np.asarray(loss)[0]))
        """
        back propagation calculation step (gradient descent)
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
    # saving training model weights into CSV files for use in the test function
    np.savetxt(filename1, weights1, delimiter=',')
    np.savetxt(filename2, weights2, delimiter=',')
    return mse


def test_model(filename1, filename2, sample_count):
    """
    Function to test the neural network
    :param filename1: First CSV file
    :param filename2: Second CSV file
    :param sample_count: The number of newly generated samples that we want to test the model on
    :return: Accuracy of the model
    """
    data = Generate(sample_count)
    # load weights into model
    weights1 = np.loadtxt(filename1, delimiter=",")
    weights2 = np.loadtxt(filename2, delimiter=",")
    correct = 0
    total = 0
    for image, label, inter_coordinates in zip(data.images, data.labels, data.intersections):
        start = []
        # extract input vector
        for ic in inter_coordinates:
            start.extend(extract_data(image, ic))
        start = np.asmatrix(start)
        """
        forward propagate data
        """
        out1 = np.dot(start, weights1.T)
        out1 = (1 / (1 + np.exp(-1 * out1)))
        out2 = np.dot(out1, weights2.T)
        out2 = (1 / (1 + np.exp(-1 * out2)))
        out2 = np.asarray(out2)
        """
        Compare output to label
        """
        if out2[0][0] > out2[0][1]:
            if label == SAFE:
                correct += 1
        else:
            if label == UNSAFE:
                correct += 1
        total += 1
    return correct / total


"""
Evaluates the accuracy of different models with varying sample sizes and learning rates.
"""
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

"""
Graphs the Average Mean Squared Error (MSE) over time of the model to show learning
"""
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
