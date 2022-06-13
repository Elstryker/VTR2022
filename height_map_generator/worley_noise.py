import numpy as np
import matplotlib.pyplot as plt


class Point2D:
    def __init__(self, x, y):
        self.p = [x, y]

    def x(self):
        return (self.p[0])

    def y(self):
        return (self.p[1])

    def distance(point1, point2):
        import math
        return (math.sqrt((point1.x() - point2.x()) ** 2 + (point1.y() - point2.y()) ** 2))

    def getDistances(origin, li: list):
        distances = []
        for ll in li:
            distances.append(Point2D.distance(origin, Point2D(ll[0], ll[1])))
        return (distances)


class WorleyNoise:

    def __init__(self, height, width, density, use_broadcast_ops):

        self.height = height
        self.width = width
        self.density = density
        self.use_broadcast_ops = use_broadcast_ops

    def auto(self, option):

        self.generatePoints()
        if self.use_broadcast_ops:
            self.broadcastCalculateNoise(option)
        else:
            self.calculateNoise(option)
        self.showNoise()

    def generatePoints(self):
        self.points = []
        for _ in range(self.density):
            self.points.append([np.random.randint(0, self.width, 1)[0], np.random.randint(0, self.height, 1)[0]])

    def showPoints(self):
        plt.scatter([self.points[i][0] for i in range(len(self.points))],
                    [self.points[l][1] for l in range(len(self.points))])
        plt.show()

    def calculateNoise(self, option):
        self.data = [[0] * self.width for _ in range(self.height)]
        for h in range(self.height):
            for w in range(self.width):
                self.distances = Point2D.getDistances(Point2D(w, h), self.points)
                self.distances.sort()
                self.data[h][w] = self.distances[option]

    def broadcastCalculateNoise(self, option):
        # casting points to numpy, it is of shape (nb_point, 2)
        points = np.array(self.points)
        # simple array of x and y coordinates for each coordinate
        xs = np.arange(self.width)
        ys = np.arange(self.height)
        # use the previously computed xs to get point.x - x for each x
        # notice the use of np.newaxis to control the broadcasting of the result to
        # an array of shape (nb_point, width)
        x_dist = np.power(points[:, 0, np.newaxis] - xs, 2)
        # same for ys, giving a (nb_point, height) shaped array
        y_dist = np.power(points[:, 1, np.newaxis] - ys, 2)
        # use the two last array to compute distance : sqrt((p.x - x) ** 2 + (.y - y ) ** 2))
        d = np.sqrt(x_dist[:, :, np.newaxis] + y_dist[:, np.newaxis, :])
        # d is of shape (nb_point, width, height), but we must sort it along the first axis
        distances = np.sort(d, axis=0)
        self.data = distances[option]

    def showNoise(self):
        import matplotlib.pyplot as plt
        plt.imshow(self.data, cmap="gray")
        plt.show()


# print("Using old fashioned loops :")
# w = WorleyNoise(height=200, width=200, density=40, use_broadcast_ops=False)
# w.auto(0)

def worley_map(width, height, density):

    w = WorleyNoise(height=height, width=width, density=density, use_broadcast_ops=True)
    w.generatePoints()
    w.broadcastCalculateNoise(0)
    w.showNoise()

    def normalizeData(data):
        return (data - np.min(data)) / (np.max(data) - np.min(data))

    data = normalizeData(w.data)

    data = np.array([[[x * 255,x * 255,x * 255] for x in elem] for elem in data])

    return data

    

