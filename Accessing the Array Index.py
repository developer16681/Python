import numpy as np

arr = np.array([
    [-1, 2, 0, 4],
    [4, -0.5, 6, 0],
    [2.6, 0, 7, 8],
    [3, -7, 4, 2.0]
])

arr2 = arr[:2, ::2]
print("First 2 rows and alternate columns:\n", arr2)

arr3 = arr[[1, 1, 0, 3], [3, 2, 1, 0]]
print("Selected elements:", arr3)