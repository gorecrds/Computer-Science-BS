from math import pi

class Shape:
   
    def __init__(self, name):
        self.name = name

    def getDescription(self):
        return self.name

    def getDimensions(self):
        return ""

    def toString(self):
        return self.name + "\t" + self.getDimensions()
    
    def __str__(self):
        return self.toString()
    
    def getShapeSize(self):
        return ()
    
    def __eq__(self, other):
        return type(self) == type(other) and self.getShapeSize() == other.getShapeSize()

class Rectangle(Shape):
   
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.height = height
        self.width = width

    def getDescription(self):
        return "Rectangle: A quadrilateral with four right angles"

    def getDimensions(self):
        return "Width: " + str(self.width) + "\tHeight: " + str(self.height)

    def getShapeSize(self):
        return tuple(sorted((self.width, self.height)))

    def area(self):
        return float(self.width * self.height)

    def perimeter(self):
        return float(2 * (self.width + self.height))


class Square(Shape):
    def __init__(self, sideLength):
        super().__init__("Square")
        self.sideLength = sideLength

    def getSideLength(self):
        return self.sideLength

    def getDescription(self):
        return "Square: A quadrilateral with four equal sides and four equal angles"

    def getDimensions(self):
        return "Side Length: " + str(self.sideLength)

    def getShapeSize(self):
        return tuple([self.sideLength])

    def area(self):
        return float(self.sideLength * self.sideLength)

    def perimeter(self):
        return float(4 * self.sideLength)


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def getDescription(self):
        return "Circle: A closed plane curve every point of which is equidistant from a fixed point within the curve"

    def getDimensions(self):
        return "Radius: " + str(self.radius)

    def getShapeSize(self):
        return tuple([self.radius])

    def area(self):
        return float(pi * self.radius * self.radius)

    def perimeter(self):
        return float(2 * pi * self.radius)

class Cylinder(Shape):
    
    def __init__(self, radius, height):
        super().__init__("Cylinder")
        self.height = height
        self.radius = radius


    def getDescription(self):
        return "Cylinder: A solid geometric figure with straight parallel sides and a circular or oval cross section"

    def getDimensions(self):
        return "Radius: " + str(self.radius) + "\tHeight: " + str(self.height)

    def getShapeSize(self):
        return (self.radius, self.height)

    def area(self):
        return float(2 * pi * self.radius * self.radius + 2 * pi * self.radius * self.height)

    def volume(self):
        return float(pi * self.radius * self.radius * self.height)


class Cube(Shape):
    def __init__(self, sideLength):
        super().__init__("Cube")
        self.sideLength = sideLength

    def getDescription(self):
        return "Cube: A three-dimensional solid object bounded by six square faces with three meeting at each vertex"

    def getDimensions(self):
        return "Side Length: " + str(self.sideLength)

    def getShapeSize(self):
        return tuple([self.sideLength])

    def area(self):
        return float(6 * self.sideLength * self.sideLength)

    def volume(self):
        return float(self.sideLength * self.sideLength * self.sideLength)

    def isTopOrBottom(self, square):
        return isinstance(square, Square) and self.sideLength == square.getSideLength()