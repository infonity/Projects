#Developed by Zeynarz
import pygame
import math

allRect = {} 

clock = pygame.time.Clock()
screen_width = 1200
screen_length = 900
grid_color = (0,0,0)
startNode_color = (2, 117, 216)
endNode_color = (240, 173, 78) 

screen = pygame.display.set_mode([screen_width,screen_length])
nothingNode = pygame.Rect(0,0,0,0)

def main():
    global pos
    global startNode
    global endNode  #Figured it out its because I didnt call global endNode here(probably when it returns from the function endNode becomes nothingNode) 
    global barrierNodes
    global chosenNode
    global foundNode
    global allSurNodes
    global allChosenNodes
    global allPossibleNodes

    startNode = nothingNode
    endNode = nothingNode
    nodeToDraw = nothingNode
    barrierNodes = []
    running = True
    algorithm_start = False
    foundNode = False
    pygame.init()
    allSurNodes = []
    allChosenNodes = {}
    allPossibleNodes = {}
    allNodeToDraw = []

    assignGrid()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONUP and endNode == nothingNode:
                pos = pygame.mouse.get_pos()
                makeNode()

            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                makeNode()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and endNode != nothingNode:
                    algorithm_start = True


        screen.fill((230,230,230))  
        if startNode !=  nothingNode:
            if endNode == nothingNode:
                pygame.draw.rect(screen,startNode_color,startNode,0)
                for rectangles in allRect:
                    if allRect[rectangles] != startNode:
                        pygame.draw.rect(screen,grid_color,allRect[rectangles],1)

            elif endNode != nothingNode: 

                if algorithm_start:
                    if not foundNode:
                        listNodes,selectedNode,cameFrom = algorithm()
                        allSurNodes.append(listNodes)
                        x , y , useless1,useless2 = selectedNode
                        if (x,y) not in allChosenNodes:
                            allChosenNodes[(x,y)] = (selectedNode,cameFrom)
                        for listOfNodes in allSurNodes:
                            for node in listOfNodes:
                                pygame.draw.rect(screen,(217, 83, 79),node,0)
                    else:
                        node1 , nodeToDraw = allChosenNodes[endX,endY]
                        while True:
                            if nodeToDraw == startNode:
                                break
                            allNodeToDraw.append(nodeToDraw)
                            x , y ,useless3 , useless4 = nodeToDraw
                            node1 , nodeToDraw = allChosenNodes[(x,y)]
                        for listOfNodes in allSurNodes:
                            for node in listOfNodes:
                                pygame.draw.rect(screen,(217, 83, 79),node,0)

                        for node in allNodeToDraw:
                            pygame.draw.rect(screen,(0,255,0),node,0)
                                                
                    
                if not barrierNodes:
                    pygame.draw.rect(screen,startNode_color,startNode,0)
                    pygame.draw.rect(screen,endNode_color,endNode,0)

                    for rectangles in allRect: 
                        if allRect[rectangles] != startNode and allRect[rectangles] != endNode:
                            pygame.draw.rect(screen,grid_color,allRect[rectangles],1)
                else:
                    pygame.draw.rect(screen,startNode_color,startNode,0)
                    pygame.draw.rect(screen,endNode_color,endNode,0)
                    for barriers in barrierNodes:
                        pygame.draw.rect(screen,grid_color,barriers,0)

                    for rectangles in allRect:
                        if allRect[rectangles] != startNode and allRect[rectangles] != endNode and allRect[rectangles] not in barrierNodes:
                            pygame.draw.rect(screen,grid_color,allRect[rectangles],1)

        else:
            for rectangles in allRect:
                pygame.draw.rect(screen,grid_color,allRect[rectangles],1)
        

        
        clock.tick(100)
        pygame.display.flip()
        
    pygame.quit()
    return 

def assignGrid():
    width = 30
    for x in range(0,screen_width,width):
        for y in range(0,screen_length,width):
            rectangle = pygame.Rect(x,y,width,width)
            allRect[(x,y)] = rectangle

    return 

def makeNode():
    global startNode
    global endNode
    global barrierNodes
    global chosenNode
    global startX
    global startY
    global endX
    global endY
    
    x1,y1 = pos
    for x2,y2 in allRect:
        if x1 in range(x2,x2 + 30 + 1):
            x3 = x2
            if y1 in range(y2,y2 + 30 + 1):
                y3 = y2
 
    if startNode == nothingNode: 
        startNode = allRect[x3,y3]
        chosenNode = startNode
        startX , startY = x3,y3
    elif startNode != nothingNode and endNode == nothingNode:
        if startNode != allRect[x3,y3]:
            endNode = allRect[x3,y3]
            endX,endY = x3,y3
    else:
        if startNode != allRect[x3,y3] and endNode != allRect[x3,y3]:
            barrierNodes.append(allRect[x3,y3])

def algorithm():
    global chosenNode
    global surNodes
    global endNode
    global foundNode
    global allPossibleNodes
    global allChosenNodes

    surNodes = [] # surrounding Nodes
    x , y, foo1 , foo2 = chosenNode
    cameFrom = chosenNode

    if not foundNode:
        for i in range(-30,30+1,30):
            for m in range(-30,30+1,30):
                if (x+i,y+m) in allRect: 
                    node = allRect[x+i,y+m]
                    if node != chosenNode and node != endNode and node not in barrierNodes and not foundNode and (x+i,y+m) not in allChosenNodes: #added this to fix barrier prob
                        surNodes.append(node)
                    elif node == endNode:
                        foundNode = True
                        algorithm_start = False
                        

    #Calculate Gcost,Hcost and Fcost
    #distance formula = square root (x1 - x2)square + (y2-y1)square
    if not foundNode:
        for x2,y2,useless1,useless2 in surNodes:
            Gcost = math.sqrt(((startX - x2)**2) + ((startY - y2)**2)) #Distance from starting Node
            Hcost = math.sqrt(((endX - x2)**2) + ((endY - y2)**2)) #Distance from ending Node
            Fcost = Gcost + Hcost
            
            allPossibleNodes[(x2,y2)] = (round(Fcost),round(Hcost))
      
        for coordinate in allChosenNodes:
            if coordinate in allPossibleNodes:
                del allPossibleNodes[coordinate]
        #still need to choose Hcost if it is lower
        for key,value in allPossibleNodes.items():
            if value == min(allPossibleNodes.values()):
                chosenNode = allRect[key]
 
    elif foundNode:
        chosenNode = endNode

    return (surNodes,chosenNode,cameFrom)

main()



