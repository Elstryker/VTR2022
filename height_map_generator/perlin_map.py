import numpy as np
from perlin_noise import PerlinNoise

def perlin_map(width,height,scale,octaves,persistance,lacunarity,seed):

    noise = PerlinNoise(octaves=1, seed=seed)
    pic = np.zeros((width,height))
    values = np.zeros((width,height))
    frequency=1
    amplitude=1
    noiseHeight=0
    min=0
    max=0
    for i in range(width):
        for j in range(height):
            for k in range(octaves):
                value = noise([i/scale*frequency, j/scale*frequency])
                noiseHeight += amplitude * value
                if value<min:
                    min=value
                if value>max:
                    max=value
                amplitude *= persistance
                frequency *= lacunarity
            values[i][j]=noiseHeight
            amplitude=1
            frequency=1
            noiseHeight=0

    for i in range(width):
        for j in range(height):
            v=(values[i][j]-min)/(max-min)*255.0
            pic[i][j] = v

    return pic