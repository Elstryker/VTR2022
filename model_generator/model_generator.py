import sys, cv2
import numpy as np

def main():
    if len(sys.argv) == 1:
        dim = int(input("Dimension: "))
        spaceVertexes = float(input("SpaceBetweenVertexes: "))
        generateGrid(dim,spaceVertexes)
        return

    elif len(sys.argv) > 2:
        print("Only one height map at a time")
        return

    texChoice = bool(int(input("0) Texture Coordinates as Whole \n1) Texture Coordinates per Vertex\n-> ")))
    amplitudeC = input("Amplitude (defaults to 30): ")
    if amplitudeC == '':
        AMPLITUDE = 30
    else:
        AMPLITUDE = float(amplitudeC)
    width = int(input("Width: "))
    height = int(input("Height: "))

    image = cv2.imread(sys.argv[1]).astype('float32')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    vertexes = calculateVertexes(image,AMPLITUDE,width,height)
    texCoords = calculateTexCoords(vertexes,texChoice)
    normals = calculateNormals(vertexes)

    generateOBJFile(vertexes,texCoords,normals)

    
def calculateVertexes(image,AMPLITUDE,width,height):
    vertexes = np.zeros(image.shape).tolist()

    stepy = float( height / (len(vertexes) -1) )
    stepx = float( width / (len(vertexes[0]) -1) )

    currentY = 0

    for i,row in enumerate(image):
        currentX = 0
        for j,height in enumerate(row):
            realHeight = ((round(height,1))/255.0) * AMPLITUDE
            vertexes[i][j] = (currentX,realHeight,currentY)
            currentX += stepx
        currentY += stepy

    return vertexes
    
def calculateTexCoords(vertexes,texChoice=False):
    if not texChoice:
        texCoords = np.zeros((len(vertexes),len(vertexes[0]))).tolist()

        stepy = float( 1.0 / (len(vertexes) -1) )
        stepx = float( 1.0 / (len(vertexes[0]) -1) )

        currentCoordY = 1

        for i in range(len(vertexes)):
            currentCoordX = 0

            for j in range(len(vertexes[i])):
                texCoords[i][j] = (round(currentCoordX,2),round(currentCoordY,2))
                currentCoordX += stepx

            currentCoordY -= stepy

        return texCoords

    else:
        texCoords = np.zeros((len(vertexes),len(vertexes[0]))).tolist()

        for i in range(len(vertexes)):
            currentCoordX = 0

            for j in range(len(vertexes[i])):
                texCoords[i][j] = (i,j)

        return texCoords
            
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def calculateNormals(vertexes):
    normals = np.zeros((len(vertexes),len(vertexes[0]))).tolist()
    
    for i,row in enumerate(vertexes):
        for j,vertex in enumerate(row):
            if j+1 == len(vertexes[i]):
                nextVX = vertexes[i][j-1]
            else:
                nextVX = vertexes[i][j+1]
            
            if i+1 == len(vertexes):
                nextVY = vertexes[i-1][j]
            else:
                nextVY = vertexes[i+1][j]

            vertex = vertexes[i][j]

            vx = normalize([nextVX[0] - vertex[0],nextVX[1] - vertex[1],nextVX[2] - vertex[2]])
            vx = [round(x,3) for x in vx]
            vy = normalize([nextVY[0] - vertex[0],nextVY[1] - vertex[1],nextVY[2] - vertex[2]])
            vy = [round(y,3) for y in vy]

            normals[i][j] = normalize(np.cross(vy,vx).tolist())
            normals[i][j] = [round(x,3) for x in normals[i][j]]

    return normals


def generateOBJFile(vertexes,texCoords,normals):
    
    objContent = ''
    for row in vertexes:
        for vertex in row:
            objRow = f'v {vertex[0]} {vertex[1]} {vertex[2]}\n'
            objContent += objRow
    
    objContent += '\n'

    for row in texCoords:
        for texCoord in row:
            objRow = f'vt {texCoord[0]} {texCoord[1]}\n'
            objContent += objRow
    
    objContent += '\n'

    for row in normals:
        for normal in row:
            objRow = f'vn {normal[0]} {normal[1]} {normal[2]}\n'
            objContent += objRow

    objContent += '\n'

    for i in range(len(vertexes)-1):
        for j in range(len(vertexes[i])-1):
            v1 = (len(vertexes[i]) * i + j) + 1
            v2 = (len(vertexes[i]) * i + j + 1) + 1
            v3 = (len(vertexes[i]) * (i+1) + j) + 1
            v4 = (len(vertexes[i]) * (i+1) + j + 1) + 1
            objRow1 = f'f {v1}/{v1}/{v1} {v3}/{v3}/{v3} {v2}/{v2}/{v2}\n'
            objRow2 = f'f {v2}/{v2}/{v2} {v3}/{v3}/{v3} {v4}/{v4}/{v4}\n'
            objContent += objRow1
            objContent += objRow2


    with open('file.obj', 'w') as f:
        f.write(objContent)
        f.flush()


def generateGrid(dim,spaceVertexes):
    num = int(dim/spaceVertexes) + 1
    currentRow = 0
    vertexes = np.zeros((num,num),dtype=object)
    for row in range(num):
        currentCol = 0
        for col in range(num):
            vertexes[row][col] = np.array([currentCol,0,currentRow])
            currentCol += spaceVertexes
        currentRow += spaceVertexes

    texCoords = calculateTexCoords(vertexes)
    normals = [[(0,1,0) for _ in range(num)] for _ in range(num)]
    generateOBJFile(vertexes,texCoords,normals)


    



if __name__ == '__main__':
    main()
