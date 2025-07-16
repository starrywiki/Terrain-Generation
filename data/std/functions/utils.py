import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage
import numpy as np
import random
import scipy.ndimage  # 确保在文件顶部导入这个库


def apply_erosion(height_map, iterations, strength):

    print("  Applying Erosion...")
    eroded_map = np.copy(height_map)  # 我们在副本上操作，不破坏原始数据

    # 创建一个3x3的卷积核，代表当前点和它周围的8个邻居
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    for _ in range(iterations):
        # 使用scipy的卷积功能，快速计算每个点与邻居的高度差
        neighbor_height_diffs = scipy.ndimage.convolve(
            eroded_map, kernel, mode="constant", cval=0
        )

        # 计算每个点应该流失的高度总量,只向比自己低的邻居流失高度
        height_loss = (
            np.maximum(0, eroded_map * 8 - neighbor_height_diffs) * strength / 8
        )

        # 更新地形
        eroded_map -= height_loss

    return eroded_map


def apply_peaks_and_valleys(height_map, intensity):

    print("  Applying Peaks and Valleys...")
    # 将高度归一化到-1到1之间
    mean_height = np.mean(height_map)
    max_deviation = np.max(np.abs(height_map - mean_height))

    if max_deviation == 0:
        return height_map

    normalized_map = (height_map - mean_height) / max_deviation
    scaled_map = normalized_map * intensity
    transformed_map = np.divide(scaled_map, (1 + np.abs(scaled_map)))

    # 将变换后的值重新映射回原来的高度范围
    new_map = transformed_map * max_deviation + mean_height

    return new_map


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
