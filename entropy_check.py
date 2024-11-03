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

# Define the block size
block_size = 256

# Calculate the entropy for each block
for i in range(0, len(data), block_size):
    block = data[i:i+block_size]
    entropy = calculate_entropy(block)
    print(f'Block {i:block_size}: Entropy = {entropy:.4f}')
