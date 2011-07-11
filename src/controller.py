#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Texwizard
from elementhandler import Elementhandler

from node import Node
from element import Element

class Controller:
    """
    The Controller class is the applications's 'workhorse'.
    All Events are routed to this class and needed informations is
    stored here. Contains lots of event handlers and code to change
    what is effictivly drawn to the Drawpanel.
    """
    def __init__(self, main):
        self.elements = []
        #helper classes
        
        self.ehandler = Elementhandler()
        self.t = Texwizard(self)
        #link
        self.main = main
        
        self.log = []
        
        #vars 
        self.leftdown = False
        self.grid = [] #redo as a class!
        self.x_shift = 20
        self.y_shift = 20
        self.gridsize = 20
        self.xnodes = 0
        self.ynodes = 0
        
        #init
        self.ehandler.Readfile('resistor') #nach handler verschieben?!
        
        self.SetGrid(50, 50, 20, 20, 10, 2)
        self.activenode = self.nodes[0]
        self.nodes[0].active = True
        self.toDraw = 'resistor'
        self.toDrawOption = 'H'
        self.lastnode = [-1, -1]
        

                
    def SetGrid(self, x, y, xnodes, ynodes, gridsize, radius): 
        self.x_shift = x
        self.y_shift = y
        self.gridsize = gridsize
        self.xnodes = xnodes
        self.ynodes = ynodes
        self.nodes = []
        for i in range(0,xnodes):
            for j in range(0, ynodes): 
                self.nodes.append(Node(i, j, radius))
        
    def PrintLog(self):
        res = ''
        for entry in self.log:
            res += entry
            res += '\n'
        return res
    
    def OnLeftClick(self, event):
        #print 'leftclick'
        if self.toDraw == 'wire': #drawing with 2 clicks
            if self.lastnode[0] >= 0:
                self.elements.append(Element('wire', '', self.lastnode[0], self.lastnode[1],
                                               self.activenode.x, self.activenode.y ))
                self.lastnode[0] = -1
            else:
                self.lastnode[0] = self.activenode.x
                self.lastnode[1] = self.activenode.y
                
        else:
            self.elements.append(Element(self.toDraw, self.toDrawOption, self.activenode.x, self.activenode.y))
        self.UpdateCanvas()
    
    def OnMouseOver(self, event):
        #highlight nodes
        x = event.GetX() - self.x_shift
        y = event.GetY() - self.y_shift
        for n in self.nodes:
            if (x - n.x * self.gridsize)**2 + (y - n.y * self.gridsize)**2 <= (n.r+2)**2:
                n.active = True
                self.activenode = n
                self.UpdateCanvas()
            else:
                n.active = False
                
    def OnWriteCodeToFile(self, event):
        print self.t.GenerateCode()
        self.t.PrintToFile('test.tex')
                
    def DrawWire(self, event):
        self.toDraw = 'wire'
        
    def DrawResistorH(self, event):
        self.toDraw = 'resistor'
        self.toDrawOption = 'H'

    def DrawResistorV(self, event):
        self.toDraw = 'resistor'
        self.toDrawOption = 'V'
    
    def UpdateCanvas(self):
        self.main.drawpanel.UpdateDrawing()
        
        
        
        
        
        
