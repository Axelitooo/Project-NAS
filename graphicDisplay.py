from easygraphics import *
import random, numpy as np

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []
    
    def distance(self, node):
        xDis = abs(self.x - node.x)
        yDis = abs(self.y - node.y)
        return int(np.sqrt((xDis ** 2) + (yDis ** 2)))
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class Edge:
    def __init__(self, nodeA, nodeB):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.length = nodeA.distance(nodeB)

    def getLength(self):
        return self.length

    def __repr__(self):
        return "(" + str(self.nodeA.x) + "," + str(self.nodeA.y) + ") " + str(self.length) + " --> (" + str(self.nodeB.x) + "," + str(self.nodeB.y) + ")"


def generateNodes(graphSizeX, graphSizeY, areaSize, nodeChancePerArea): 
    nodeList = []

    # generates node homogeneously in a grid while avoiding generating nodes to close from each other
    for i in range(graphSizeX//areaSize):
        for j in range(graphSizeY//areaSize):
            if (random.random() < 0.5):
                node = Node(x=int((random.random()*0.8 + i + 0.1) * areaSize), y=int((random.random()*0.8 + j + 0.1) * areaSize))
                # print(str(node))
                nodeList.append(node)

    return nodeList

def generateLinks(nodeList, maximalDistance):
    # generates links
    for node in nodeList:
        for otherNode in nodeList:
            if otherNode != node:
                if node.distance(otherNode) < maximalDistance:
                    node.edges.append(Edge(node, otherNode))

def runWorld(graphSizeX = 50, graphSizeY = 50, areaSize = 5, nodeChancePerArea = 0.1, maximalDistance = 12):
    nodeList = generateNodes(graphSizeX, graphSizeY, areaSize, nodeChancePerArea)
    generateLinks(nodeList, maximalDistance)

    set_color(Color.BLACK)
    set_fill_color(Color.WHITE)

    while is_run():
        if delay_jfps(60):
            clear_device()
            for node in nodeList:
                for edge in node.edges:
                    move_to(edge.nodeA.x/graphSizeX * 1280, edge.nodeA.y/graphSizeY * 960)
                    line_to(edge.nodeB.x/graphSizeX * 1280, edge.nodeB.y/graphSizeY * 960)

def main():
    init_graph(1280, 960)
    set_render_mode(RenderMode.RENDER_MANUAL)
    runWorld()
    close_graph()

easy_run(main)

