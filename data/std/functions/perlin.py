import math
import numpy as np
from utils import fade, lerp
from defs import *

def generate_randvec2(nlattice: int) -> np.ndarray:
    randtable = np.random.randint(NRANDVEC, size = (nlattice, nlattice))
    return RANDVEC2_TABLE[randtable]

### Task1: Naive 2D Perlin
### Hint: Gradient vectors, the fade function, and linear interpolation
class PerlinNoise:
    seed: int
    lattice_size: int
    nmap: int
    nlattice: int
    randvec2: np.ndarray
    
    def __init__(self, seed: int, lattice_size: int = 128, nmap: int = 4):
        pass
        

    def get_perlin(self, x: float, z: float) -> float:
        w = 0.0
        ### Code begins here
        
        
        ### Code ends here
        return w
        
        

### Task2-1: Octaveal 2D Perlin
### Hint: Use multiple perlin noise generators with different lattice sizes and nmap

def GeneratePerlinNoiseArray(octaves: int, lattice_size: int = 128, nmap: int = 4) -> list:
    ret = []
    
    ### Your code begins here
    
    
    ### Your code ends here
        
    return ret

def get_perlin_octave(x: float, z: float, perlin_array: list) -> float:
    # Generate the 2D perlin noise with octaves
    noise = 0
    ### Your code begins here


    ### Your code ends here
    return noise