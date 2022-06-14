import perlin_map, open_simplex_noise, random_noise, worley_noise
import cv2
from datetime import datetime

def handler(opt):
    handlers = {
        "1" : get_perlin_map,
        "2" : get_open_simplex_map,
        "3" : get_random_noise_map,
        "4" : get_worley_noise_map
    }

    if opt in handlers:
        handlers[opt]()
    else:
        print("Inválid Option!!")

def menu():
    opts = ("""
Choose type of map:

4 - Worley Map
3 - Random Noise Map
2 - Open Simplex Map
1 - Perlin Map
0 - Leave
\n> """)

    opt = input(opts)
    if (opt=="0") :
        print("Goodbye!")
        return 0
    handler(opt)
    menu()

def get_perlin_map():
    width = int(input("Width: "))
    height = int(input("height: "))
    scale = float(input("scale: "))
    octave = int(input("octaves: "))
    persistance = float(input("persistance: "))
    lacunarity = float(input("lacunarity: "))
    seed = int(input("seed: "))
    img_path = input("img path: ")


    pic = perlin_map.perlin_map(width,height,scale,octave,persistance,lacunarity,seed)
    cv2.imwrite(img_path,pic)
    print("\nImage created with success!")

def get_random_noise_map():

    width = int(input("Width: "))
    height = int(input("height: "))
    img_path = input("img path: ")

    try:
        seed = int(input("seed: "))
        if seed == '' or seed == ' ':
            seed = int(datetime.now().timestamp())
    except:
        seed = int(datetime.now().timestamp())

    pic = open_simplex_noise.open_simplex_map(width,height,seed)
    cv2.imwrite(img_path,pic)
    print("\nImage created with success!")

def get_open_simplex_map():

    width = int(input("Width: "))
    height = int(input("height: "))
    img_path = input("img path: ")

    try:
        seed = int(input("seed: "))
        if seed == '' or seed == ' ':
            seed = int(datetime.now().timestamp())
    except:
        seed = int(datetime.now().timestamp())

    pic = random_noise.random_map(width,height,seed)
    cv2.imwrite(img_path,pic)
    print("\nImage created with success!")

def get_worley_noise_map():

    width = int(input("Width: "))
    height = int(input("height: "))
    density = int(input("density: "))
    img_path = input("img path: ")

    pic = worley_noise.worley_map(width,height,density)
    cv2.imwrite(img_path,pic)
    print("\nImage created with success!")


menu()