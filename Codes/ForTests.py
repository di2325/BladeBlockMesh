import os
import numpy as np
import matplotlib.pyplot as plt

coordN = 0
indexN = 0

airfoilNumber = 5

for line in open(os.path.abspath(f'../Coordinates/airfoil{airfoilNumber}'), "r"):
    if line.startswith('v'):
        coordN += 1
    elif line.startswith('l'):
        indexN += 1

# print(coordN, indexN)
coord = np.zeros(shape=(coordN,3))
index = np.zeros(shape=(indexN,2))

i = 0
j = 0
for line in open(os.path.abspath(f'../Coordinates/airfoil{airfoilNumber}'), "r"):
    # Assing Coordinates
    if line.startswith('v'):
        coord[i] = ((round(float(line.split()[1]), 4), \
                      round(float(line.split()[2]), 4), \
                      round(-1.0 * float(line.split()[3]), 4)))
        i += 1
    # Assign Indices
    elif line.startswith('l'):
        index[j] = ((int(line.split()[1]) - 1, int(line.split()[2]) - 1))
        j += 1

print(coord)
mostLeftID = np.argmax(coord[:, 0])
mostLeft = coord[mostLeftID]
mostRightID = np.argmin(coord[:, 0])
mostRight = coord[mostRightID]
print(mostLeft)
print(mostRight)

# plt.scatter(coord[:, 0], coord[:, 1])
# plt.gca().invert_xaxis()
# plt.show()

# print("Coord")
# print(coord[0])
# print("Index")
# print(index[0])