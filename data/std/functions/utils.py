import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage
import numpy as np
import random

# Utility Functions for Minecraft Commands
f = open("test.mcfunction", "w")


def setblock(x: int, y: int, z: int, block_name: str):
    print("setblock {} {} {} minecraft:".format(x, y, z) + block_name, file=f)


def fill(x: int, y_min: int, y_max: int, z: int, block_name: str):
    print(
        "fill {} {} {} {} {} {} minecraft:".format(x, y_min, z, x, y_max, z)
        + block_name,
        file=f,
    )


def plant_tree(top_array: np.ndarray, x_max: int, z_max: int):
    # Plant trees at random locations
    # Not required to be implemented, but you can use this function as an option for decoration
    # this function will plant 50 trees at random locations, this will not work if the terrain is too steep
    # therefore, you should figure out a clever way to determine where to plant trees
    for _ in range(50):  # Plant 50 trees
        x = random.randint(0, x_max)
        z = random.randint(0, z_max)
        y = int(top_array[x][z])
        setblock(x, y + 1, z, "oak_sapling")


# Linear interpolation, alpha refers to the distance to val1
def lerp(val1: float, val2: float, alpha: float) -> float:
    return val1 * (1 - alpha) + val2 * alpha


# Fade function to smooth the transition between different lattice cells
def fade(x: float) -> float:
    return x * x * x * (x * (x * 6 - 15) + 10)


# Visualize the generated terrain
# So you don't need to boot up Minecraft to see the result
def visualize(height_array: np.ndarray, x_max: int, z_max: int):
    plt.rcParams["figure.figsize"] = (5, 5)
    # Create a 3D visualization of the terrain
    x_coords, z_coords = np.meshgrid(np.arange(x_max), np.arange(z_max))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("3D Minecraft-like Terrain with Grassland Sinusoidal Patterns")
    terrain_plot = ax.scatter(
        x_coords, z_coords, height_array, c=height_array, cmap="terrain", marker="."
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Y")

    plt.show()
