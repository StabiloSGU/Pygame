from math import sqrt


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.length = magnitude(self)
        self.normalized = False

    def __repr__(self):
        return '2DVector('+str(self.x)+', '+str(self.y)+') length of '+str(self.length)

    def mul(self, scalar):
        result = Vector(self.x*scalar, self.y*scalar)
        return result

    def show(self):
        print(self.x, self.y)


def magnitude(vector):
    return round(sqrt(vector.x**2+vector.y**2), 2)


def vectorsum(*vectors):
    resultingx = 0
    resultingy = 0
    for vector in vectors:
        resultingx += vector.x
        resultingy += vector.y
    resultingvector = Vector(resultingx, resultingy)
    return resultingvector


v = Vector(-1.6, 0)
v.show()