from math import sqrt
from math import acos


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.length = vectorlength(self)

    def __repr__(self):
        return 'Vector('+str(self.x)+', '+str(self.y)+') and length of '+str(self.length)+'.'

    def mul(self, multiplier):
        collinear = Vector(self.x * multiplier, self.y * multiplier)
        return collinear

    def __mul__(self, multiplier):
        self.x *= multiplier
        self.y *= multiplier

    def __rmul__(self, multiplier):
        self.__mul__(multiplier)

    def normalize(self):
        if self.x == 0 and self.y == 0:
            print('Magnitude is zero, cannot normalize vector')
        else:
            self.x /= self.length
            self.y /= self.length
            self.length = vectorlength(self)

    def show(self):
        print(self.x, self.y)


def vectorsum(*vectors):
    resultingx = 0
    resultingy = 0
    for vector in vectors:
        resultingx += vector.x
        resultingy += vector.y
    resultingvector = Vector(resultingx, resultingy)
    return resultingvector


# use to find speed of objects with speed vector of 'vector'
def vectorlength(vector):
    return sqrt(vector.x*vector.x + vector.y*vector.y)


def distance(vector1, vector2):
    return sqrt((vector1.x-vector2.x)**2+(vector1.y-vector2.y)**2)


def scalardirection(vector1, vector2):
    return vector1.x*vector2.x + vector1.y+vector2.y


def scalarangle(vector1, vector2):
    vector1.normalize()
    vector2.normalize()
    len1 = vectorlength(vector1)
    len2 = vectorlength(vector2)
    scaldir = scalardirection(vector1, vector2)
    theta = acos(scaldir/(len1 * len2))
    return theta


D = Vector(1, 1)
D.show()
G = Vector(1, 3)
G.show()
H = Vector(3, 2)
H.show()
V = vectorsum(H, G.mul(-1))
V.show()
