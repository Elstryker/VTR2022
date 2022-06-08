import perlin_map

def handler(opt):
    handlers = {
        "1" : get_perlin_map
    }

    if opt in handlers:
        handlers[opt]()
    else:
        print("Inválid Option!!")

def menu():
    opts = ("""
Choose type of map:

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
    img_path = input("img path: ")
    seed = int(input("seed: "))
    octave = int(input("octave: "))


    perlin_map.perlin_map(width,height,img_path,seed,octave)
    print("\nImage created with success!")

menu()