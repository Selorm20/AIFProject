from LibraryRiccardo import *

def CreateBooleanMatrix(x, y):
    Result = []
    for i in range(y):
        Result.append([True for i in range(x)])
    return Result

def PrintBooleanMatrix(Matrix):
    for i in Matrix:
        for r in i:
            if(r): print("V ", end = "")
            else:  print("X ", end = "")
        print("")
    
#Traps like tuples (x, y)
def ApplyFalseToMatrix(Matrix, Traps):
    for i in Traps:
        Matrix[i[1]][i[0]] = False
            
def ApplyTrueToMatrix(Matrix, Traps):
    for i in Traps:
        Matrix[i[1]][i[0]] = True
        
Matrix = CreateBooleanMatrix(5, 5)

def GetNeighbourPointsFunctionMatrix(Point):
    
    Result = [(Point[0]-1, Point[1]-1), (Point[0]-1, Point[1]+1), (Point[0]-1, Point[1]), (Point[0], Point[1]-1),
              (Point[0]+1, Point[1]-1), (Point[0]+1, Point[1]+1), (Point[0]+1, Point[1]), (Point[0], Point[1]+1)]
    
    Result = list(filter(lambda i: i[1] >= 0 and i[1] < len(Matrix[0]) and i[0] >= 0 and i[0] < len(Matrix) and Matrix[i[1]][i[0]], Result))
     
    return Result

SearchPath1 = AstarPathSearch(GetNeighbourPointsFunctionMatrix)

assert SearchPath1.CalculatePath((0, 0), (4, 4)) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

ApplyFalseToMatrix(Matrix, [(1, 1)])

assert SearchPath1.CalculatePath((0, 0), (4, 4)) == [(0, 0), (1, 0), (2, 1), (3, 2), (4, 3), (4, 4)]

ApplyFalseToMatrix(Matrix, [(2, 1), (3, 1)])

assert SearchPath1.CalculatePath((0, 0), (4, 4)) == [(0, 0), (0, 1), (1, 2), (2, 3), (3, 4), (4, 4)]

ApplyFalseToMatrix(Matrix, [(1, 0), (0, 1)])

assert SearchPath1.CalculatePath((0, 0), (4, 4)) == None

ApplyTrueToMatrix(Matrix, [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1)])

SearchPath2 = BFSPathSearch(GetNeighbourPointsFunctionMatrix)

assert SearchPath1.CalculatePath((0, 0), (4, 4)) in SearchPath2.CalculatePath((0, 0), [(4, 4)])[(4, 4)]

ApplyFalseToMatrix(Matrix, [(1, 1)])

assert SearchPath1.CalculatePath((0, 0), (4, 4)) in SearchPath2.CalculatePath((0, 0), [(4, 4)])[(4, 4)]

ApplyFalseToMatrix(Matrix, [(2, 1), (3, 1)])

assert SearchPath1.CalculatePath((0, 0), (4, 4)) in SearchPath2.CalculatePath((0, 0), [(4, 4), (3, 2)])[(4, 4)]
assert SearchPath1.CalculatePath((0, 0), (3, 2)) in SearchPath2.CalculatePath((0, 0), [(4, 4), (3, 2)])[(3, 2)]

ApplyFalseToMatrix(Matrix, [(1, 0), (0, 1)])

assert SearchPath2.CalculatePath((0, 0), [(4, 4)]) == {(4, 4): []}

ApplyTrueToMatrix(Matrix, [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1)])

ApplyFalseToMatrix(Matrix, [(1, 1)])