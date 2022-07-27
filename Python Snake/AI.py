import numpy as np
from AStarObject import node
#this class is used to calculate next move
#DROW and DCOL is uused to check adjacent nodes
DROW=[-1,0,1,0]
DCOL=[0,1,0,-1]
def getMove(Board,applocRow,applocCol,HeadlocRow,HeadLocCol):#A* algo to determine the next move
    valBoard=np.empty((80,80),dtype=node)#create a 2d array of nodes
    for r in range (80):
        for c in range (80):
            valBoard[r][c]=node(r,c)
    openList=[]
    closedList=[]
    #set all the values of the first node
    valBoard[HeadlocRow][HeadLocCol].setG(0)
    valBoard[HeadlocRow][HeadLocCol].setH(getDist(HeadlocRow,HeadLocCol,applocRow,applocCol))
    valBoard[HeadlocRow][HeadLocCol].setF(valBoard[HeadlocRow][HeadLocCol].getG()+valBoard[HeadlocRow][HeadLocCol].getH())
    openList.append(valBoard[HeadlocRow][HeadLocCol])
    found=False
    while(len(openList)!=0 and found==False): #stop the A* if we run out of nodes to search or goal is found
        openList.sort(key=lambda x: x.getF()) #sort the open list from smallest to largest using the weights of each node as the point of sorting
        curr=openList.pop(0) #get the top of the list
        closedList.append(curr) #add it to the closed list (ie nodes we wont search again)
        for i in range(len(DCOL)): #check adjacent nodes
            rD=curr.getRow()+DROW[i] #varaibles to make it easier to type
            cD=curr.getCol()+DCOL[i]
            if(rD>=0 and rD<80 and cD>=0 and cD<80): #make sure we are still in bounds
                if(rD==applocRow and cD==applocCol): #if we find the solution
                    #update all the values of the node and stop the loop
                    found=True
                    valBoard[rD][cD].setG(curr.getG()+1)
                    valBoard[rD][cD].setH(getDist(rD,cD,applocRow,applocCol))
                    valBoard[rD][cD].setF(valBoard[rD][cD].getG()+valBoard[rD][cD].getH())
                    valBoard[rD][cD].setParent(curr)
                    openList.append(valBoard[rD][cD])
                else:#else
                    if(valBoard[rD][cD] not in closedList): #if the adjacent node isnt in the closed list
                        if(Board[rD][cD]==0): #ensure that the node we are checking is actually open (does not work for some reason???)
                            if(valBoard[rD][cD] not in openList): #if the current node isnt in the open list
                                #set all the values and add it to the open list
                                valBoard[rD][cD].setG(curr.getG()+1)
                                valBoard[rD][cD].setH(getDist(rD,cD,applocRow,applocCol))
                                valBoard[rD][cD].setF(valBoard[rD][cD].getG()+valBoard[rD][cD].getH())
                                valBoard[rD][cD].setParent(curr)
                                openList.append(valBoard[rD][cD])
                            elif(valBoard[rD][cD].getF()>((curr.getG()+1)+(getDist(rD,cD,applocRow,applocCol)))): #if the node is in the open list AND the current F value of that node is less than the F value in the open list
                                #find the nodes position in the open liset
                                index=openList.index(valBoard[rD][cD])
                                openList.pop(index) #and remove it from the open list
                                #recalculate all values for said node and readd it to the open list
                                valBoard[rD][cD].setG(curr.getG()+1)
                                valBoard[rD][cD].setH(getDist(rD,cD,applocRow,applocCol))
                                valBoard[rD][cD].setF(valBoard[rD][cD].getG()+valBoard[rD][cD].getH())
                                valBoard[rD][cD].setParent(curr)
                                openList.append(valBoard[rD][cD])

    finalPosRow=applocRow
    finalPosCol=applocRow
    pos=valBoard[applocRow][applocCol].getParent() #get the node the apple is loacted in
    if(pos.getParent()==None): #if it doesnt have a parent, no path exists return 8 (a random number i picked to represent no path)
        return 8
    else: #if a path does exist
        while(pos.getParent().getLoc() !=(HeadlocRow,HeadLocCol)):#trace the path back until we are at the node just infront of the head and get the coords
            finalPosRow=valBoard[applocRow][applocCol].getRow()
            finalPosCol=valBoard[applocRow][applocCol].getCol()
            pos=pos.getParent()
    
        if(HeadLocCol==finalPosCol): #if the path and the head is in the same coloumn
            if(HeadlocRow>finalPosRow): #and the head is above
                return(0)#return 0
            else:
                return(2) #if below return 1
        else: #if they are in different rows, it means they are in the same coloumn same logic applies as above
            if(HeadLocCol>finalPosCol):
                return(3)
            else:
                return(1)

def getDist(Row,Col,endRow,endCol): #this function returns the manhattan distance between 2 points (used for H)
    h=np.abs(Col-endCol)+np.abs(Row-endRow)
    return h
