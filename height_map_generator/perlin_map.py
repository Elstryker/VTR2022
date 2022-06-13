import numpy as np
from perlin_noise import PerlinNoise

def perlin_map(width,height,seed,octaves):

    noise = PerlinNoise(octaves=octaves, seed=seed)
    pic = np.zeros((width,height,3))

    for i in range(width):
        for j in range(height):
            value = (noise([i/width, j/height])+1)*127.5
            for k in range(3):
                pic[i][j][k] = value

    return pic