class Body:#a class that stores all the data needed for the player position
    def __init__(self,head,row,col) :
        self.isHead=head #boolean on whether or not this is a the head
        self.row=row
        self.col=col
        self.parent=None
        self.dir=1
    def setParent(self,parent):
        self.parent=parent
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def getLoc(self): #gets the row and coloumn in 1 line, mostly used for debugging
        return (self.row,self.col)
    def setLoc(self,row,col):#update the position of the piece of the snake in the world
        if(self.isHead==True):#if its the head set the position to the newly given position
            self.row=row
            self.col=col
        else:#if it is part of the body set the position to the parents position
            self.row=self.parent.getRow()
            self.col=self.parent.getCol()
            self.setDir(self.parent.dir)
    def getParent(self):
        if(self.isHead):
            return None
        else:
            return self.parent
    def getDir(self): #the direction this piece is moving
        return self.dir
    def setDir(self,dir):
        self.dir=dir