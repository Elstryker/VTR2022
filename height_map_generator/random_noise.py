import numpy as np
import random


def random_map(width, height, seed):

    random.seed(seed)

    def noise():
        return random.randrange(255)

    value = np.zeros((width,height,3))
    for y in range(height):
        for x in range(width):
            noiseValue = noise()
            for z in range(3):
                value[x][y][z] = noiseValue

    return value