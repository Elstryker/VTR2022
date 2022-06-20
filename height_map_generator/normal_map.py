import sys, cv2
from cv2 import norm
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

    nmap=generate_normal_map(image)
    cv2.imwrite("nmap.png",nmap)
    print("\nNormal map created with success!")

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
    
def generate_normal_map(image):
    
    normal_map = np.zeros((image.shape[0],image.shape[1],3))
    print(image)

    for i, row in enumerate(image):
        for j, height in enumerate(row):
            if (i == image.shape[0]-1 or i == 0 or j == image.shape[1]-1 or j == 0):
                normal_map[i][j] = (127.5,255,127.5)
            else:
                hlu = image[i-1][j] 
                hld = image[i+1][j]
                hcl = image[i][j-1]
                hcr = image[i][j+1]
                diffl = hld-hlu
                diffc = hcr-hcl
                dx = (0,diffc,2)
                dy = (2,diffl,0)
                normal = (normalize(np.cross(dx,dy))+(1)) * 127.5
                normal_map[i][j] = normal
    

    return(normal_map)
            

main()
