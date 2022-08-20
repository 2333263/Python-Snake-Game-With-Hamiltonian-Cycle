
class node: #the nodes needed for the A star algorithm
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.G=0 #distance from head
        self.parent=None
        self.F=0 #G+H
        self.H=0 #distance from goal
        #the rest of the functions either return a value or set a value
    def setG(self,val):
        self.G=val
    def getG(self):
        return self.G
    def getRow(self):
        return self.row
    def getCol(self):
        return self.col
    def getLoc(self):
        return(self.row,self.col)
    def setParent(self,parent):
        self.parent=parent
    def getParent(self):
        return self.parent
    def setF(self):
        self.F=-(self.G+self.H) #note the negative is so the heap is a maxiumum heap not a minumum heap
    def getF(self):
        return self.F
    def getH(self):
        return self.H
    def setH(self,h):
        self.H=h
    def __lt__(self,nxt):
        return self.F>nxt.F #this used by the heap, so it knows what values to compare when items are added to it
