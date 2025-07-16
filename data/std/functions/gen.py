# import every function in utils.py and perlin.py
from utils import *
from perlin import *
import random
import math
import numpy as np


### Task2-2: Spline method
### Hint: Simulate "Continentalness"
### This is the spline table for plain biome
spline_table_plain = {
    -1.0: 5,
    -0.5: 15,
    0.0: 25,
    0.5: 35,
    1.0: 45,
}

spline_table_plataeu = {
    -1.0: 120,
    -0.5: 110,
    0.0: 100,
    0.5: 80,
    1.0: 60,
}

spline_table_mountain = {
    -1.0: 10,
    -0.5: 40,
    0.0: 80,
    0.5: 120,
    1.0: 150,
}


def spline(noise: float, spline_table: dict) -> float:
    keys = sorted(spline_table.keys())
    if noise < keys[0]:
        return spline_table[keys[0]]
    if noise > keys[-1]:
        return spline_table[keys[-1]]
    for i in range(len(keys) - 1):
        if keys[i] <= noise <= keys[i + 1]:
            x0, x1 = keys[i], keys[i + 1]
            y0, y1 = spline_table[x0], spline_table[x1]
            alpha = (noise - x0) / (x1 - x0)
            return lerp(y0, y1, alpha)


print("Starting terrain generation...")
print(f"xm:{x_max},zm:{z_max}")
random.seed(666)

# clear all
print("fill {} -64 {} {} 256 {} air".format(0, 0, x_max, z_max), file=f)

height_array = np.zeros((x_max, z_max))
noise_array = np.zeros((x_max, z_max))

# This array keeps track of the top block's height (either grass or water)
top_array = np.zeros((x_max, z_max))

# Generate the perlin noise array, with max_octaves = 3
PerlinNoiseArray = GeneratePerlinNoiseArray(
    seed_=789, octaves=3, lattice_size=4, nmap=128
)

transition_start = 0.08  # 低于此值为山脉
transition_end = 0.63  # 高于此值为山峰

for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    for z in range(0, z_max):
        # noise = perlin.get_perlin(x, z)
        noise1 = get_perlin_octave(x, z, PerlinNoiseArray)
        peaks_height = int(noise1 * 300.0)
        mount_height = int(noise1 * 60 + 13)
        if noise1 > transition_end:
            final_height = peaks_height
        elif noise1 < transition_start:
            final_height = mount_height
        else:
            alpha = (noise1 - transition_start) / (transition_end - transition_start)
            smooth_alpha = fade(alpha)
            final_height = lerp(mount_height, peaks_height, smooth_alpha)
            # height = int(spline(noise, spline_table_plataeu))
        height_array[x][z] = int(final_height)

print("Base terrain generated. Now applying post-processing layers...")


# 强化山峰和山谷，让地形特征更明显
height_array = apply_peaks_and_valleys(height_array, intensity=1.2)
height_array = apply_erosion(height_array, iterations=8, strength=0.5)


for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    for z in range(0, z_max):
        # 从处理后的数组中获取最终高度，并转为整数
        height = int(height_array[x][z])
        water_covered = False

        fill(x, -10, height, z, "stone")
        fill(x, height + 1, height + 4, z, "dirt")

        # fill water until y=0
        if height + 5 <= 0:
            water_covered = True
            fill(x, height + 5, 0, z, "water")

        if not water_covered:
            setblock(x, height + 5, z, "grass_block")
            top_array[x][z] = height + 5
        else:
            top_array[x][z] = 0

# plant_tree(top_array, x_max, z_max)

visualize(height_array, x_max, z_max)
