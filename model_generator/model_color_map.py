import sys, cv2
import numpy as np
from scipy.special import comb

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
    blue = (0.525*255,0,0)
    green = (0.15*255,0.76*255,0.3*255)
    brown = (0.125*255,0.35*255,0.65*255)
    white = (0.98*255,0.98*255,0.98*255)
    
    color_map = np.zeros((image.shape[0],image.shape[1],3))

    for i,row in enumerate(image):
        for j,height in enumerate(row):
            if (height>0.85*255):
                color_map[i][j] = white
            elif (height>0.55*255):
                x = smoothstep(height,0.55*255,0.85*255,5)
                color_map[i][j] = mix(brown,white,x)
            elif (height>0.20*255):
                x = smoothstep(height,0.20*255,0.55*255,5)
                color_map[i][j] = mix(green,brown,x)
            else:
                x = smoothstep(height,0,0.20*255,5)
                color_map[i][j] = mix(blue,green,x)

    return color_map
    


def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)

    result = 0
    for n in range(0, N + 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result

def mix(fir,sec,interpol):
    ret = [fir[0] * (1 - interpol) + sec[0] * interpol, fir[1] * (1 - interpol) + sec[1] * interpol, fir[2] * (1 - interpol) + sec[2] * interpol]
    return ret

if __name__ == "__main__":
    main()