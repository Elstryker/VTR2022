from opensimplex import OpenSimplex
from opensimplex.constants import DEFAULT_SEED
import numpy as np

def open_simplex_map(width, height, seed=DEFAULT_SEED):

    def noise(nx, ny):
        gen = OpenSimplex(seed)
        # Rescale from -1.0:+1.0 to 0.0:1.0
        return gen.noise2(nx, ny) / 2.0 + 0.5

    value = np.zeros((width,height,3))
    for y in range(height):
        for x in range(width):
            nx = (x - 0.5) / 50 # Dividing x by width will decrease the frequency
            ny = (y - 0.5) / 50 # Same as above
            noiseValue = noise(nx, ny) * 255
            for z in range(3):
                value[x][y][z] = noiseValue

    return value