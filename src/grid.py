#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# grid.py - implementation of the Grid class
# 

from node import Node

class Grid:
    """
    Grid class holds information for the grid.
    """
    def __init__(self, x_size=20, y_size=20, nodedistance=15, 
                 x=20, y=20):
        self.x_size = x_size
        self.y_size = y_size
        self.ndist = nodedistance
        self.x = x
        self.y = y
        self.an = None #activenode
        self.ln = None #lastnode
        self.nodes = []
        self.changeNodes(self.x_size, self.y_size, self.ndist)
        
    def changeNodes(self, x_size, y_size, nodedistance):
        self.x_size = x_size
        self.y_size = y_size
        self.ndist = nodedistance
        self.an = None
        self.ln = None
        
        for i in range(0,self.x_size):
            for j in range(0, self.y_size): 
                self.nodes.append(Node(i, j))
                
    def findActiveNode(self, x, y):
        x = x - self.x
        y = y - self.y
        g = int(self.ndist / 2)**2+1 #precalculated radius
        gs = self.ndist
        
        if self.an == None:
            for n in self.nodes:
                if (x - n.x * gs)**2 + (y - n.y * gs) **2 <= g:
                    self.an = n
                    return True
        else:
            if (x - self.an.x * gs)**2 + (y - self.an.y * gs) **2 > g:
                #self.ln = self.an
                for n in self.nodes:
                    if (x - n.x * gs)**2 + (y - n.y * gs) **2 <= g:
                        self.an = n
                        return True
            else:
                return False
        self.an = None
        return True