from shape import Rectangle, Square, Circle, Cylinder, Cube

rectangle1 = Rectangle(3, 4)
rectangle2 = Rectangle(4, 3)
rectangle3 = Rectangle(5, 6)
square1 = Square(2)
square2 = Square(4)
square3 = Square(4)
circle1 = Circle(3)
circle2 = Circle(5)
cylinder1 = Cylinder(3, 5)
cylinder2 = Cylinder(4, 6)
cylinder3 = Cylinder(6, 4)
cube1 = Cube(2)
cube2 = Cube(3)

shapeList = [
    rectangle1, rectangle2, rectangle3,
    square1, square2, square3,
    circle1, circle2,
    cylinder1, cylinder2, cylinder3,
    cube1, cube2
]

print("*****PRINTING OUT THE TEXT REPRESENTATION, DESCRIPTION, AREA, AND PERIMETER/VOLUME OF EACH SHAPE")
for shape in shapeList:
    print(shape)
    print(shape.getDescription())
    print("\tArea:", shape.area())
    
    if isinstance(shape, Rectangle) or isinstance(shape, Square) or isinstance(shape, Circle):
        print("\tPerimeter:", shape.perimeter())

    if isinstance(shape, Cylinder) or isinstance(shape, Cube):
        print("\tVolume:", shape.volume())
    
    print("")

print("\n*****PRINTING ALL EQUAL, NON-ALIAS SHAPES")
for firstShape in shapeList:
    for secondShape in shapeList:
        if firstShape == secondShape and firstShape is not secondShape:
            print("Equal shapes found: ")
            print("\t" + str(firstShape))
            print("\t" + str(secondShape))
        
print("\n*****PRINTING ALL CUBE/SQUARE COMBINATIONS WHERE THE SQUARE IS A SIDE FOR THE CUBE")
for firstShape in shapeList:
    for secondShape in shapeList:
        if isinstance(firstShape, Square) and isinstance(secondShape, Cube):
            if secondShape.isTopOrBottom(firstShape):
                print("Square-Cube Match Found:")
                print("\t" + str(firstShape))
                print("\t" + str(secondShape))


print("\n*****PRINTING ALL COMBINATIONS OF TWO-DIMENSIONAL SHAPES THAT CAN FIT INSIDE ANOTHER")
for firstShape in shapeList:
    for secondShape in shapeList:
        break
        # EXTRA CREDIT: TEST THE canFitInside METHOD FOR PAIRS OF TWO DIMENSIONAL SHAPES. PRINT ANY SHAPES THAT NEST.