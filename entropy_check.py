import numpy as np
import math

def calculate_entropy(data):
    # Calculate the probability distribution of each byte value
    probabilities = np.unique(data, return_counts=True)
    probabilities = probabilities[1] / len(data)

    # Calculate the entropy
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return entropy

# Load the binary data
data = np.fromfile('data/DB_1116.gdb')

# Calculate the entropy
entropy = calculate_entropy(data)
print('Entropy:', entropy)