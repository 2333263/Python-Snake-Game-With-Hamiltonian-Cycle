from msilib.schema import Error
import pygame as pg
import numpy as np
from Player import Body
import AI as ai
pg.init()
height=800
width=800
Screen=pg.display.set_mode((width,height))
clock=pg.time.Clock()
PlayButton=pg.Rect(250,400,300,50)
AIPlayButton=pg.Rect(250,500,300,50)
#for reference its board[row][col]
board=np.zeros((40,40),dtype=int)
Head=Body(True,20,20)
board[20][20]=1 #start the player at the middle of the board
prev=Head
growTick=6
dir=1 #used for direction snake head is moving in, 0 is up, 1 is right, 2 down, 3 is left
for i in range(3): #this for loop just adds 3 body parts behind the head
    temp=Body(False,20,20-(i+1))
    temp.setParent(prev)
    board[20][20-(i+1)]=1
    prev=temp
Tail=prev #keep track of the tail
win=False
play=False
AI=False

def printBoard(): #prints the bored in console used for debugging
    for i in range(40): #row
        temp=""
        for j in range(40): #col
            temp+=str(board[i][j])
        print(temp)

def drawScreen(): #this draws the state of the board to the screen, each element of the baord represents a 10x10 block of pixels
    for r in range(40):
        for c in range(40):
            if(board[r][c]==1): #if there is a snake in this location
                pg.draw.rect(Screen,(255,0,0),pg.Rect(20*c,20*r,20,20)) #draw it in red
            elif(board[r][c]==2): #apples
                pg.draw.rect(Screen,(0,255,0),pg.Rect(20*c,20*r,20,20)) #green
 #this function randomly generations a position of an apple
def getAppleLoc():
    positions=[]#list of empty spots of the board
    for i in range (40): #loop through the board
        for j in range(40):
            if(board[i][j]==0): #if there is a spot with nothing on it add it to the list
                positions.append((i,j))
    if(len(positions)==0): #if the list is empty by the end return -1 -1 which is an indicator the player has won
        return((-1,-1))
    else: #else pick one of the spots at random and return it
        pos=np.random.randint(0,len(positions))
        return(positions[pos])
    
appLoc=getAppleLoc()#get the new apple location
board[appLoc[0]][appLoc[1]]=2 #sets its position on the bored
#if the bored is entirely snake, the player wins
def checkWin():
    for r in range(40):
        for c in range(40):
            if(board[r][c]!=1):
                return(False)
    return(True)


path=np.zeros((40,40))

while True: #animation loop
    for event in pg.event.get():
        if event.type==pg.QUIT: #on close, quit the game
            pg.quit()
            exit()
        elif event.type==pg.KEYDOWN and AI==False: #if the ai is not playing and it detects a keypress
            if(win==False): #and the player has not won
                if(event.key==pg.K_UP and dir!=2): #if the player presses up and the snake isnt going down
                    dir=0#change direction to up
                elif(event.key==pg.K_LEFT and dir!=1): #same as above for left
                    dir=3
                elif(event.key==pg.K_RIGHT and dir!=3): #same as above for right
                    dir=1
                elif(event.key==pg.K_DOWN and dir!=0): #same as above for right
                    dir=2
            else: #if the player has won and the player pressed r, restart the game
                if(event.key==pg.K_r):
                    growTick=6
                    board=np.zeros((40,40),dtype=int)
                    Head=Body(True,20,20)
                    board[20][20]=1
                    prev=Head

                    dir=1 #used for direction snake head is moving in, 0 is up, 1 is right, 2 down, 3 is left
                    for i in range(3):
                        temp=Body(False,20,20-(i+1))
                        temp.setParent(prev)
                        board[20][20-(i+1)]=1
                        prev=temp
                    Tail=prev
                    lost=False
                    appLoc=getAppleLoc()
                    board[appLoc[0]][appLoc[1]]=2
            if(event.key==pg.K_ESCAPE): #if the player ever pressed escape close the game
                pg.quit()
                exit()
            Head.setDir(dir) #update the direction of the head
        elif event.type==pg.MOUSEBUTTONDOWN: #if a mouse is clicked
            if(event.button==1 and PlayButton.collidepoint(pg.mouse.get_pos())==True): #and its on the play button
                play=True #start the game
            elif(event.button==1 and AIPlayButton.collidepoint(pg.mouse.get_pos())==True): #and its on the AI button
                AI=True #start the game with the ai running
                play=True
                path=ai.generateHamCycle(20,20) #when the use clicks the ai button, a hamiltonian cycle will be generated
    if(play==True):#if the game has started
        if(win==False):
            headRow=Head.getRow() #for ease of access
            headCol=Head.getCol()
            lost=False #if the player has lost the game
            Screen.fill((0,0,0)) #empty the screen
            drawScreen() #redraw it
            if(AI==True): #if the ai is running
                prevDir=dir #store prev direction
                dir=ai.retMove(path,Head.getRow(),Head.getCol()) #the next move is generated by the ai
                if(dir==8): #if there is no possible move, continue in the direction the snake was already going
                    dir=prevDir
                Head.setDir(dir) #update the head direction
            #updates the position of the snake every frame
            if(dir==0 and (headRow-1)>=0): #moving up
                board[Tail.getRow()][Tail.getCol()]=0
                curr=Tail
                while(curr.isHead==False):
                    curr.setLoc(0,0) #setting the body positions so input values dont matter
                    curr=curr.getParent()
                board[headRow-1][headCol]=1
                Head.setLoc(headRow-1,headCol)
            elif(dir==1 and headCol+1<40): #moving right
                
                board[Tail.getRow()][Tail.getCol()]=0
                curr=Tail
                while(curr.isHead==False):
                    curr.setLoc(0,0) #setting the body positions so input values dont matter
                    curr=curr.getParent()
                board[headRow][headCol+1]=1
                Head.setLoc(headRow,headCol+1)
                
            elif(dir==2 and headRow+1<40): #moving down
                curr=Tail
                board[Tail.getRow()][Tail.getCol()]=0
                while(curr.isHead==False):
                    curr.setLoc(0,0) #setting the body positions so input values dont matter
                    curr=curr.getParent()
                board[headRow+1][headCol]=1
                Head.setLoc(headRow+1,headCol)
            elif(dir==3 and headCol-1>=0): #moving left
                curr=Tail
                board[Tail.getRow()][Tail.getCol()]=0
                while(curr.isHead==False):
                    curr.setLoc(0,0) #setting the body positions so input values dont matter
                    curr=curr.getParent()
                board[headRow][headCol-1]=1
                Head.setLoc(headRow,headCol-1)
            else:
                #hit the wall, lose the game
                lost=True
            curr=Tail
            #hit your body lose the game
            while(curr.parent!=None):
                if(Head.getLoc()==curr.getLoc()):
                    lost=True
                    break
                else:
                    curr=curr.getParent()

            if(lost==True): #if the game is lost just reset the playing field
                growTick=6
                board=np.zeros((40,40),dtype=int)
                Head=Body(True,20,20)
                board[20][20]=1
                prev=Head

                dir=1 #used for direction snake head is moving in, 0 is up, 1 is right, 2 down, 3 is left
                for i in range(3):
                    temp=Body(False,20,20-(i+1))
                    temp.setParent(prev)
                    board[20][20-(i+1)]=1
                    prev=temp
                Tail=prev
                lost=False
                appLoc=getAppleLoc()
                board[appLoc[0]][appLoc[1]]=2
            if(Head.getLoc()==appLoc): #if an apple is eaten
                if(checkWin()): #check if the player has won
                    win=True
                else: #if not
                    growTick=0 #set the growth ticks to 0, is explained better later
                    appLoc=getAppleLoc() #get new position of the apple
                    if(appLoc==(-1,-1)):
                        win=True
                    else:
                        board[appLoc[0]][appLoc[1]]=2
            if(growTick<5): #each time the player eats an apple, they grow by 5 units, but instead of doing this isntantly, it grows over the span of 5 iterations of the game
            
                TailDir=Tail.getDir()#get direction of the tail
                tempTail=None #create a temp tail
                #depending on the direction the tail is moving, place the new tail relative to that
                Succeed=False
                iter=0
                while (Succeed==False and iter<4): #in case the tail is up against the wall
                    #the code will try grow the tail in every possible direction, before giving up and declaring the player a winner
                    
                    if(TailDir==0):
                        if(Tail.getRow()+1>=40):
                            TailDir+=1
                            iter+=1
                        else:
                            tempTail=Body(False,Tail.getRow()+1,Tail.getCol())
                            Succeed=True
                    elif(TailDir==1):
                        if(Tail.getCol()-1<0):
                            TailDir+=1
                            iter+=1
                        else:
                            tempTail=Body(False,Tail.getRow(),Tail.getCol()-1)
                            Succeed=True
                    elif(TailDir==2):
                        if(Tail.getRow()-1<0):
                            TailDir+=1
                            iter+=1
                        else:
                            tempTail=Body(False,Tail.getRow()-1,Tail.getCol())
                            Succeed=True
                    elif(TailDir==3):
                        if(Tail.getCol()+1>=40):
                            TailDir=0
                            iter+=1
                        else:
                            tempTail=Body(False,Tail.getRow(),Tail.getCol()+1)
                            Succeed=True
                if(Succeed==True):
                    tempTail.setDir(TailDir) #set the direction of the new tail
                    tempTail.setParent(Tail) #set the parent of the tail to be the old tail
                    Tail=tempTail #set the pointer to the tail to be the new tail
                    board[tempTail.getRow()][tempTail.getCol()]=1 #add it to the board
                    growTick+=1 #up the growth tick by 1
                else:
                    win=True
                    growTick=6
               
        else:
            if(AI==False):
                Screen.fill((0,0,0))
                font=pg.font.Font("freesansbold.ttf",32)
                text=font.render("You Win, Press r to restart",True,(255,255,255)) #you win text on screen
                Screen.blit(text,(250,300))
            else:
                win=False
                growTick=6
                board=np.zeros((40,40),dtype=int)
                Head=Body(True,20,20)
                board[20][20]=1
                prev=Head

                dir=1 #used for direction snake head is moving in, 0 is up, 1 is right, 2 down, 3 is left
                for i in range(3):
                    temp=Body(False,20,20-(i+1))
                    temp.setParent(prev)
                    board[20][20-(i+1)]=1
                    prev=temp
                Tail=prev
                lost=False
                appLoc=getAppleLoc()
                board[appLoc[0]][appLoc[1]]=2
    else: #if were in the menu, place all the text and buttons on the screen
        font=pg.font.Font("freesansbold.ttf",32)
        text=font.render("Welcome to Snake",True,(255,255,255))
        Screen.blit(text,(250,200))
        text=font.render("Play",True,(255,255,255))
        pg.draw.rect(Screen,(90,90,90),PlayButton)
        Screen.blit(text,(375,409))
        pg.draw.rect(Screen,(90,90,90),AIPlayButton)
        text=font.render("AI Play",True,(255,255,255))
        Screen.blit(text,(355,509))
    
    pg.display.flip()

    clock.tick(30) #lock frame rate to 30fps
    


