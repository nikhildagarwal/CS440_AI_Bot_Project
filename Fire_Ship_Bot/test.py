from typing import List

import matplotlib.pyplot as plt
import numpy as np

# Generate data points for acidity and sweetness
acidity_values = np.linspace(-6, 3, 100)
sweetness_values = np.linspace(-3, 3, 100)

# Create a meshgrid for plotting
acidity, sweetness = np.meshgrid(acidity_values, sweetness_values)

# Define the decision boundary
decision_boundary = acidity == -3

# Plotting the decision boundary
plt.contour(acidity, sweetness, decision_boundary, levels=[0], colors='black')

# Plotting the decision regions
plt.fill_between(acidity_values, -3, 3, where=(acidity_values >= -3), color='orange', alpha=0.3, label='Lemon')
plt.fill_between(acidity_values, -3, 3, where=(acidity_values < -3), color='green', alpha=0.3, label='Lime')

# Labeling axes and adding legend
plt.xlabel('Acidity')
plt.ylabel('Sweetness')
plt.legend()

# Show the plot
plt.show()

