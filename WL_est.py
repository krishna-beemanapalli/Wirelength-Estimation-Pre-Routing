from math import sqrt

points = []
graph = []

def findSmallest(key, mstSet): 
  
        min = float("inf")
        
        for v in range(len(graph)): 
            if key[v] < min and mstSet[v] == False: 
                min = key[v] 
                min_index = v 
  
        return min_index

    
def getMSTWeight(parent):
    global graph
    weight = 0
    for i in range(1, len(graph)):
        weight = weight + graph[i][parent[i]]
        
    return weight


def primMST(): 
    global graph
    key = [float("+inf")] * len(graph)
    parent = [None] * len(graph)
    key[0] = 0 
    mstSet = [False] * len(graph)

    parent[0] = -1  

    for cout in range(len(graph)): 

        u = findSmallest(key, mstSet) 

        mstSet[u] = True

        for v in range(len(graph)): 

            if graph[u][v] > 0 and mstSet[v] == False and key[v] > graph[u][v]: 
                    key[v] = graph[u][v] 
                    parent[v] = u 

    return getMSTWeight(parent) 

def findLeftMostPoint(points):
    return sorted(points)[0]
    
def findRightMostPoint(points):
    return sorted(points)[-1]

def findTopMostPoint(points):
    return sorted(points, key = lambda x : x[1])[-1]

def findBottomMostPoint(points):
    return sorted(points, key = lambda x : x[1])[0]

def findTopLeftPoint(topPoint, leftPoint):
    return [leftPoint[0], topPoint[1]]

def findTopRightPoint(topPoint, rightPoint):
    return [rightPoint[0], topPoint[1]]

def findBottomLeftPoint(bottomPoint, leftPoint):
    return [leftPoint[0], bottomPoint[1]]

def findDist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    
    return abs(x2 - x1) + abs(y2 - y1)

def HPWL(points):
    
    leftPoint = findLeftMostPoint(points)
    topPoint = findTopMostPoint(points)
    bottomPoint = findBottomMostPoint(points)
    rightPoint = findRightMostPoint(points)

    rectTopLeftPoint = findTopLeftPoint(topPoint, leftPoint)
    rectBottomLeftPoint = findBottomLeftPoint(bottomPoint, leftPoint)
    rectTopRightPoint = findTopRightPoint(topPoint, rightPoint)

    rectLength = findDist(rectTopLeftPoint, rectBottomLeftPoint)
    rectBreadth = findDist(rectTopLeftPoint, rectTopRightPoint)

    return rectLength + rectBreadth

def getSteinerPoints(points):

    steinerPoints = []

    for pt1 in points:
        for pt2 in points:
            if pt1 == pt2:
                continue
            
            x1, y1 = pt1
            x2, y2 = pt2

            steiner_pt1 = [x1, y2]
            steiner_pt2 = [x2, y1]
            if steiner_pt1 not in points + steinerPoints:
                steinerPoints.append(steiner_pt1)

            if steiner_pt2 not in points + steinerPoints:
                steinerPoints.append(steiner_pt2)

    return steinerPoints
            

def computeMST(points):
    global graph
    adjMatrix = []

    for point1 in points:
        adjMatrix.append([])
        for point2 in points:
            adjMatrix[-1].append(findDist(point1, point2))

    graph = adjMatrix
    return primMST()
    

with open("net7", "r") as file:
    lines = file.read().split("\n")

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        
        nums = line.split(" ")
        points.append([int(nums[0]), int(nums[1])])
print ("# Points: " + str(len(points)))
print ("HPWL: " + str(HPWL(points)))
currentMST_weight = computeMST(points)
print ("MST: " + str(currentMST_weight))
while True:

    bestMST = currentMST_weight + 1
    bestSteinerPoint = []
    steinerPoint = getSteinerPoints(points)

    for s_pt in steinerPoint:
        MSTwt = computeMST(points + [s_pt])
        if MSTwt < bestMST:
            bestMST = MSTwt
            bestSteinerPoint = s_pt

    if bestMST < currentMST_weight:
        currentMST_weight = bestMST
        points = points + [bestSteinerPoint]
    else:
        break

print("Steiner tree: " + str(currentMST_weight))
