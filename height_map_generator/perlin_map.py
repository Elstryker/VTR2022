import cv2
import numpy as np
from perlin_noise import PerlinNoise

def perlin_map(width,height,file_path,seed,octaves):

    noise = PerlinNoise(octaves=octaves, seed=seed)
    pic = np.array([[((noise([i/width, j/height])+1)*127.5) for j in range(width)] for i in range(height)])

    cv2.imwrite(file_path,pic)