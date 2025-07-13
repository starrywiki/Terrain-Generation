import math
import numpy as np
from utils import fade, lerp
from defs import *
import random


def generate_randvec2(nlattice: int) -> np.ndarray:
    randtable = np.random.randint(NRANDVEC, size=(nlattice, nlattice))
    return RANDVEC2_TABLE[randtable]


### Task1: Naive 2D Perlin
### Hint: Gradient vectors, the fade function, and linear interpolation
class PerlinNoise:
    seed: int
    lattice_size: int
    nmap: int
    nlattice: int
    randvec2: np.ndarray

    # x_max = z_max = 512 = lattice_size * nmap
    def __init__(self, seed: int, lattice_size: int, nmap: int):
        self.seed = seed
        self.lattice_size = lattice_size
        self.nmap = nmap
        self.nlattice = 1 + nmap
        random.seed(seed)
        self.randvec2 = generate_randvec2(self.nlattice)

    def get_perlin(self, x: float, y: float) -> float:
        fx = x / self.nlattice
        fy = y / self.nlattice

        x0 = int(fx)
        y0 = int(fy)

        x1 = x0 + 1
        y1 = y0 + 1

        dx = fx - x0
        dy = fy - y0
        """
        01 11
        00 10
        """
        g00 = self.randvec2[x0 % self.nlattice][y0 % self.nlattice]
        g10 = self.randvec2[x1 % self.nlattice][y0 % self.nlattice]
        g01 = self.randvec2[x0 % self.nlattice][y1 % self.nlattice]
        g11 = self.randvec2[x1 % self.nlattice][y1 % self.nlattice]

        d00 = np.array([dx, dy])
        d10 = np.array([dx - 1, dy])
        d01 = np.array([dx, dy - 1])
        d11 = np.array([dx - 1, dy - 1])

        s = np.dot(g00, d00)
        t = np.dot(g10, d10)
        u = np.dot(g01, d01)
        v = np.dot(g11, d11)

        fade_dx = fade(dx)
        fade_dy = fade(dy)

        a = lerp(s, t, fade_dx)
        b = lerp(u, v, fade_dx)
        w = lerp(a, b, fade_dy)

        return w


### Task2-1: Octaveal 2D Perlin
### Hint: Use multiple perlin noise generators with different lattice sizes and nmap


def GeneratePerlinNoiseArray(octaves: int, lattice_size: int, nmap: int) -> list:
    ret = []
    for i in range(octaves):
        ls = lattice_size * (2**i)
        nm = 512 // ls
        perlin = PerlinNoise(seed=698 + i, lattice_size=ls, nmap=max(1, nm))
        ret.append(perlin)
    return ret


def get_perlin_octave(x: float, z: float, perlin_array: list) -> float:
    # Generate the 2D perlin noise with octaves
    noise = 0
    amplitude = 1.0  # 影响度
    total_amplitude = 0.0
    for octave in perlin_array:
        noise += amplitude * octave.get_perlin(x, z)
        total_amplitude += amplitude
        amplitude *= 0.5
    noise /= total_amplitude
    return noise
