import sys, cv2
import numpy as np


def main():
    if len(sys.argv) == 1:
        print("Height Map need to be specified")
        return

    elif len(sys.argv) > 2:
        print("Only one height map at a time")
        return

    image = cv2.imread(sys.argv[1]).astype('float32')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cmap=generate_color_map(image)
    cv2.imwrite("cmap.png",cmap)
    print("\nColor map created with success!")


    
def generate_color_map(image):
    blue = (0.525*255.2*255,0,0)
    green = (0.15*255,0.76*255,0.3*255)
    brown = (0.125*255,0.35*255,0.65*255)
    white = (0.98*255,0.98*255,0.98*255)
    
    color_map = np.zeros((image.shape[0],image.shape[1],3))

    for i,row in enumerate(image):
        for j,height in enumerate(row):
            if (height>0.85*255):
                color_map[i][j] = white
            elif (height>0.55*255):
                color_map[i][j] = brown
            elif (height>0.20*255):
                color_map[i][j] = green
            else:
                color_map[i][j] = blue

    return color_map
    
main()