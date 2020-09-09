#!/usr/bin/python3
import sys

class Node:
    char=''
    gCost=0
    hCost=0
    pos=(0,0)
    parent=None

    def __init__(self, char):
        self.char = char
    
    def fCost(self):
        return self.gCost + self.hCost

def isStartSquare(c):
    if (c == 'S'):
        return True
    return False

def isEndSquare(c):
    if (c == 'E'):
        return True
    return False

def isWallSquare(c):
    if (c == 'X'):
        return True
    return False

# Calculate the heuristic distance between two nodes
def distance(nodeOne, nodeTwo):
    oneX, oneY = nodeOne.pos
    twoX, twoY = nodeTwo.pos
    distX = abs(oneX - twoX)
    distY = abs(oneY - twoY)
    if (distX > distY):
        return 14*distY + 10*(distX-distY)
    return 14*distX + 10*(distY-distX)

# Follow parent nodes from end node to start which will follow the shortest path
# while changing the associated character to asterisks to visualize the shortest path
def drawPath(start, end):
    cur = end
    while (cur != start):
        if (cur != end):
            cur.char = '*'
        cur = cur.parent


grid=[]
if (len(sys.argv) > 1):
    fileName=sys.argv[1]
else:
    print('No file found in executable command')
    exit()

# Read grid file and store each character as a node in a 2d list
with open(fileName, 'r') as fp:
        line = []
        while True:
            c = fp.read(1)
            if not c:
                break
            if (c == '\n'):
                grid.append(line)
                line = []
            else:
                node = Node(c)
                line.append(node)

start=None
end=None

print('Entered grid from file:')
# Print grid and set start/end nodes
for i in range(len(grid)):
    for j in range(len(grid[i])):
        c = grid[i][j].char
        grid[i][j].pos = (i,j)
        print(c, end="")
        if (isStartSquare(c)):
            start = grid[i][j]
        elif (isEndSquare(c)):
            end = grid[i][j]
        
    print()

if (not start or not end):
    print('\nFile given not following correct format please enter start and end characters')
    exit()

openNodes= []
closedNodes = set()
openNodes.append(start)

while(len(openNodes) > 0):
    cur = openNodes[0]
    for i in range(len(openNodes)):
        # Change the current node if there is another node in open set with lower costs
        if (openNodes[i].fCost() < cur.fCost() or openNodes[i].fCost() == cur.fCost() and openNodes[i].hCost < cur.hCost):
            cur = openNodes[i]
    
    openNodes.remove(cur)
    closedNodes.add(cur)

    # Once current node has reached end, Draw the path on grid and exit the loop
    if (cur == end):
        drawPath(start, end)
        break
    
    posX, posY = cur.pos
    # Scan neighbouring nodes of current calculating their costs
    for i in range(posX-1, posX+2):
        for j in range(posY-1, posY+2):
            if (i < 0 or j < 0 or i >= len(grid) or j >= len(grid[i]) or i == posX and j == posY or isWallSquare(grid[i][j].char) or grid[i][j] in closedNodes):
                continue
            moveCost = cur.gCost + distance(cur, grid[i][j])
            # Calculate costs if node is not in open set or recalculate if their is a shorter route
            if (moveCost < grid[i][j].gCost or not grid[i][j] in openNodes):
                grid[i][j].gCost = moveCost
                grid[i][j].hCost = distance(grid[i][j], end)
                grid[i][j].parent = cur

                if (not grid[i][j] in openNodes):
                    openNodes.append(grid[i][j])

print('\nSolution to given grid:')
# Print grid after completing pathfind or not being able to find pathfind
for i in range(len(grid)):
    for j in range(len(grid[i])):
        c = grid[i][j].char
        print(c, end="")        
    print()