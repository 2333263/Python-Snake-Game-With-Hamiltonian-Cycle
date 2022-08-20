import numpy as np
from AStarObject import node
import heapq
#this class is used to calculate next move
#DRow and DCol is uused to check adjacent nodes
DRow=[-1,0,1,0]
DCol=[0,1,0,-1]

def getMoves(board,row,col): #when presented with partially complete board, and a position
    #all valid positions that can be moved into are put into a list 
    moves=[]
    for i in range (len(DRow)):
        if(row+DRow[i]<40 and row+DRow[i]>=0 and col+DCol[i]<40 and col+DCol[i]>=0):
            if(board[row+DRow[i]][col+DCol[i]]==0):
               moves.append((row+DRow[i],col+DCol[i]))
    return moves

def getDist(Row,Col,enDRow,enDCol): #this function returns the manhattan distance between 2 points (used for H)
    h=np.abs(Col-enDCol)+np.abs(Row-enDRow)
    return h

def checkDone(board): #checks if the hamiltonian cycle is complete, but checking that each node has been visted
    for i in range (len(board)):
        for j in range(len(board[0])):
            if(board[i][j]==0):
                return False
    return True

def Astar(board,StartRow,StartCol,EndRow,EndCol): #this is an A star seach, that finds the furthest path from one position to another position
    #the way the furthest path is found is that when F is set in the AstarObject class, the real F value is multiplied by negative one
    #so on the heap, the largest values are on the top instead of the smallest, which priorizes the longest route

    valBoard=np.empty((40,40),dtype=node) #generate a board of nodes
    for i in range(40):
        for j in range(40):
            valBoard[i][j]=node(i,j)
    openList=[]
    heapq.heapify(openList) #create a heap which acts a priority queue
    closedList=[] #and createa a closed list
    valBoard[StartRow][StartCol].setG(0) #set the distance from start pos to be 0 for the first node
    valBoard[StartRow][StartCol].setH(getDist(StartRow,StartCol,EndRow,EndCol)) #calculate distance to end node
    valBoard[StartRow][StartCol].setF() #add G and H together and multiply by negative 1
    heapq.heappush(openList,valBoard[StartRow][StartCol]) #push the node to the heal
    found=False 
    while(len(openList)!=0 and found==False):
        curr=heapq.heappop(openList) #pop the largest node off the heap
        closedList.append(curr) #add it to the closed list
        for i in range(len(DRow)): #in every direction around that node
            rD=curr.getRow()+DRow[i] #these are just so i didnt have to type out curr.getRow()+DRow[i] a hundred times
            rC=curr.getCol()+DCol[i]

            if(rD>=0 and rD<40 and rC>=0 and rC<40): #if the sorrounding position is valid
                if(rD==EndRow and rC==EndCol): #if the new position is the end
                    found=True #end the loop
                    valBoard[EndRow][EndCol].setG(curr.getG()+1) #set the final cost of the path (to make this a pure search algorithm, change this to set the parent of the final node to curr and then trace back from the final node)
                else: #if its not the final position
                    if(valBoard[rD][rC] not in closedList): #if the new node isnt in the closed list
                        if(board[rD][rC]==0): #and the spot is open on the board
                            if(valBoard[rD][rC] not in openList): # and we havent already checked the node in the open list
                                valBoard[rD][rC].setG(curr.getG()+1) 
                                valBoard[rD][rC].setH(getDist(rD,rC,EndRow,EndCol))
                                valBoard[rD][rC].setF()
                                valBoard[rD][rC].setParent(curr)
                                 #set all of its values, and set its parent to be curr
                                heapq.heappush(openList,valBoard[rD][rC]) #and add it to the max heap
                            elif(valBoard[rD][rC].getF()>((curr.getG()+1)+(getDist(rD,rC,EndRow,EndCol)))): #if the node has been checked already, but this has a lower value
                                index=openList.index(valBoard[rD][rC]) #get its position on the heap
                                openList[index].F=-1 #set its F value to be -1 so it will be ontop of the heap
                                openList.pop() #remove it from the heap
                                heapq.heapify(openList) #rebuild the heap, to ensure the ordere is correct
                                valBoard[rD][rC].setG(curr.getG()+1) 
                                valBoard[rD][rC].setH(getDist(rD,rC,EndRow,EndCol))
                                valBoard[rD][rC].setF()
                                valBoard[rD][rC].setParent(curr)
                                #set all the new values and add it to the heap
                                heapq.heappush(openList,valBoard[rD][rC])
    return (valBoard[EndRow][EndCol].getG()) #return how many steps this path is going to take
    #again to make this a pure path finder, trace back from the final node to the root, adding each node to a list and return the list


#this function generates a hamiltonian cycle
def generateHamCycle(HeadLocRow,HeadLocCol):
    path=np.zeros((40,40)) #create an empty board
    path[HeadLocRow][HeadLocCol]=1 #set the start position to be 1
    prevposRow=HeadLocRow #set the current position to the start position
    prevposCol=HeadLocCol
    prevVal=1 #set the current step value to be 1
    while(not checkDone(path)): #while the path is incomplete
        Found=False #Assume no path
        moves=getMoves(path,prevposRow,prevposCol) #get all possible moves at current position
        if(len(moves)>0): #if there are possible moves to make
            prevVal+=1 #increase the step counter
            dist=0 #set a largest dist to be 0
            dists=[] #an array to store the coordinates that will be moved into next
            for i in range(len(moves)): #for every possible move
                temp=Astar(path,moves[i][0],moves[i][1],HeadLocRow,HeadLocCol) #get how many steps it will take, on the longest path, to return to the start, if we go in this direction
                if(temp>dist): #if that cost is greater than our current highest cose
                    dist=temp #set the current best path to be the new one
                    dists=moves[i]
            path[dists[0]][dists[1]]=prevVal #set the new positions cost value
            prevposRow=dists[0] #set the current coordinates to the new coordinates
            prevposCol=dists[1]
            Found=True #path in this step was found
    if(Found==False):
        print("None Found")
    else:
        return(path) #return the board with the path on it
        

def retMove(path,currRow,currCol): #given a board and some coordinates, this function will return the direction needs to go to follow the path
    val=path[currRow][currCol]+1 #get the current value and add one
    if(val>40*40): #if it greater than the number of tiles on the board set it to 1
        val=1 #this is so we when we get to the end of the cycle it start it over
    for i in range(len(DRow)): #for every node around the current node
        if(currRow+DRow[i]>=0 and currRow+DRow[i]<40 and currCol+DCol[i]>=0 and currCol+DCol[i]<40): #that is a valid node
            if(path[DRow[i]+currRow][DCol[i]+currCol]==val): #if we find the next position we have to return to 
                return i #return that direction
    return 8 #else return no valid move
            

