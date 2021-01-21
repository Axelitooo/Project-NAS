from easygraphics import *
import random, numpy as np

from storage import MemoryStorage
from token_bucket import TokenBucket
from router import Router
from calendarQueue import CalendarQueue, SimulatedTime

def distance(x1, y1, x2, y2):
    xDis = abs(x1 - x2)
    yDis = abs(y1 - y2)
    return int(np.sqrt((xDis ** 2) + (yDis ** 2)))

def generateRouters(graphSizeX, graphSizeY, areaSize, routerChancePerArea, rate, capacity, calendarQueue): 
    routerList = {}
    routerId = 0

    # generates routers homogeneously in a grid while avoiding generating routers to close from each other
    for i in range(graphSizeX//areaSize):
        for j in range(graphSizeY//areaSize):
            if (random.random() < routerChancePerArea):
                storage = MemoryStorage()
                bucket = TokenBucket(rate, capacity, storage)

                x = int((random.random()*0.5 + i + 0.25) * areaSize)
                y = int((random.random()*0.5 + j + 0.25) * areaSize)

                router = Router(routerId, x, y, state=True, tokenBucket=bucket, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue, linkStates=None)
    
                routerList[routerId] = router
                routerId+=1

    return routerList

def generateLinks(routerList, maximalDistance):
    # generates links
    for routerId in routerList:
        for otherRouterId in routerList:
            if otherRouterId != routerId:
                dist = distance(routerList[routerId].x, routerList[routerId].y, routerList[otherRouterId].x, routerList[otherRouterId].y)
                if dist < maximalDistance:
                    routerList[routerId].add_neighbour(otherRouterId, dist, dist)

def runWorld(graphSizeX = 50, graphSizeY = 50, areaSize = 10, routerChancePerArea = 0.5, maximalDistance = 30, rate = 10, capacity = 100):
    simu = SimulatedTime(0)
    myCalendarQueue = CalendarQueue(simu)

    routerList = generateRouters(graphSizeX, graphSizeY, areaSize, routerChancePerArea, rate, capacity, myCalendarQueue)
    generateLinks(routerList, maximalDistance)

    set_color(Color.BLACK)
    set_fill_color(Color.WHITE)

    myCalendarQueue.scheduler.run()

    while is_run():
        if delay_jfps(60):
            clear_device()
            for routerId in routerList:
                for neighbourId in routerList[routerId].neighbours:
                    x1 = routerList[routerId].x/graphSizeX * 1280
                    y1 = routerList[routerId].y/graphSizeY * 800
                    x2 = routerList[neighbourId].x/graphSizeX * 1280
                    y2 = routerList[neighbourId].y/graphSizeY * 800

                    move_to(x1, y1)
                    line_to(x2, y2)

                    xMid = (x1 + x2)/2
                    yMid = (y1 + y2)/2
                    if y1 > y2:
                        yMid -= 5
                    else:
                        yMid += 20

                    draw_text(xMid, yMid, routerList[routerId].neighbours[neighbourId][0])
                    # move_to(xMid + (x1 + x2)/20, yMid + (y1 + y2)/20)
                    # line_to(xMid + (x1 + x2)/10, yMid + (y1 + y2)/10)

                # draw_text(x1, y1 - 10, str(routerList[routerId].buffer.qsize()) + "/" + str(routerList[routerId].bufferSize))


def main():
    init_graph(1280, 800)
    set_render_mode(RenderMode.RENDER_MANUAL)
    runWorld()
    close_graph()

easy_run(main)