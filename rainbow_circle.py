import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define radii and center
R1 = 0.2  # Interior white circle radius
R2 = 0.3  # Outer radius
center = (0.9, 0.9)  # Center of the circle (x, y)

# Create a custom colormap from white to blue
cmap = LinearSegmentedColormap.from_list("WhiteRedBlue", ["white", "red", "blue"])

# Generate points within the outer circle
resolution = 500
x = np.linspace(center[0] - R2, center[0] + R2, resolution)
y = np.linspace(center[1] - R2, center[1] + R2, resolution)
x, y = np.meshgrid(x, y)
distances = np.sqrt((x - center[0])**2 + (y - center[1])**2)

# Create a mask for points within the outer circle radius
mask_outer = distances <= R2
x = x[mask_outer]
y = y[mask_outer]
distances = distances[mask_outer]

# Create a mask for points within the inner circle radius
mask_inner = distances <= R1

# Normalize distances for points between R1 and R2
distances_normalized = np.zeros_like(distances)
distances_normalized[~mask_inner] = (distances[~mask_inner] - R1) / (R2 - R1)

# Plotting
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=distances_normalized, cmap=cmap, marker='.')
ax.set_aspect('equal', 'box')
ax.axis('off')  # Hide the axes
plt.xlim(center[0] - R2, center[0] + R2)
plt.ylim(center[1] - R2, center[1] + R2)
plt.show()
