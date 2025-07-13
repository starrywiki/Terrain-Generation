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
PerlinNoiseArray = GeneratePerlinNoiseArray(3, lattice_size=4, nmap=128)

# perlin = PerlinNoise(seed=789, lattice_size=8, nmap=64)

for x in range(0, x_max):
    if x % 32 == 0:
        print("x = {}".format(x))
    for z in range(0, z_max):
        # noise = perlin.get_perlin(x, z)
        noise = get_perlin_octave(x, z, PerlinNoiseArray)
        # noise = PerlinNoiseArray[1].get_perlin(x, z)
        # height = int(noise * 80.0 + 5)
        height = int(spline(noise, spline_table_plataeu))

        height_array[x][z] = height
        noise_array[x][z] = noise
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
