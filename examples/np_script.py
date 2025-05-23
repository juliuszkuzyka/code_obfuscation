import numpy as np
import matplotlib.pyplot as plt

# === Good basis (trapdoor/private) ===
B_good = np.array([[1, 0], [0, 1]])  # Standard basis (orthogonal)

# === Unimodular matrix (det = ±1) ===
U = np.array([[2, 3], [1, 2]])

# === Bad basis (public) ===
B_bad = U @ B_good  # Still spans the same lattice

print(B_bad)

# === Generate lattice points (same lattice for both) ===
range_val = 8
points = []
for i in range(-range_val, range_val):
    for j in range(-range_val, range_val):
        point = i * B_good[0] + j * B_good[1]
        points.append(point)
points = np.array(points)

# === Plotting ===
plt.figure(figsize=(8, 8))
plt.scatter(points[:, 0], points[:, 1], s=14, color='blue', label='Lattice Points', zorder=10)

origin = np.array([[0, 0], [0, 0]])

# Good basis in green (thinner arrows)
plt.quiver(*origin, B_good[:, 0], B_good[:, 1],
           angles='xy', scale_units='xy', scale=1,
           color='green', label='Good Basis',
           width=0.01, headwidth=3, headlength=4, zorder=15)

print()
# Bad basis in red (thinner arrows)
plt.quiver(*origin, B_bad[0, :], B_bad[1, :], angles='xy', scale_units='xy', scale=1,color='red', label='Bad Basis', width=0.01, headwidth=3, headlength=4, zorder=15)

# Axes and aesthetics
plt.axhline(0, color='black', linewidth=0.5, zorder=5)
plt.axvline(0, color='black', linewidth=0.5, zorder=5)
plt.grid(True, zorder=0)
plt.gca().set_aspect('equal', adjustable='box')
#plt.title('Same Lattice with Good and Bad Bases (Lattice-Based Crypto)')
#plt.legend()
plt.show()
