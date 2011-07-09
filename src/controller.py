#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Element
from elementhandler import Elementhandler

class Node:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.active = False

class Controller:
    def __init__(self, main, texwizard):
        self.log = []
        self.t = texwizard
        self.main = main
        self.leftdown = False
        self.grid = []
        self.x_shift = 0#10
        self.y_shift = 0#10
        self.gridsize = 20
        self.ehandler = Elementhandler()
        self.ehandler.Readfile('resistor') #nach handler verschieben?!
        #self.ehandler.ShowElements() #debugging
        self.SetGrid(10, 10, 40, 40, 15, 2)
        self.activenode = self.nodes[0]
        self.nodes[0].active = True
        self.toDraw = 'resistor'
        self.toDrawOption = 'H'
        self.lastnode = [-1, -1]
        

                
    def SetGrid(self, x, y, xnodes, ynodes, gridsize, radius): 
        self.x_shift = x
        self.y_shift = y
        self.gridsize = gridsize
        self.nodes = []
        for i in range(0,xnodes):
            for j in range(0, ynodes): 
                self.nodes.append(Node(i * self.gridsize + x, j * self.gridsize + y, radius))
        
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
                self.t.elements.append(Element('wire', '', self.lastnode[0], self.lastnode[1],
                                               self.activenode.x, self.activenode.y ))
                self.lastnode[0] = -1
            else:
                self.lastnode[0] = self.activenode.x
                self.lastnode[1] = self.activenode.y
                
        else:
            self.t.elements.append(Element(self.toDraw, self.toDrawOption, self.activenode.x, self.activenode.y))
        self.UpdateCanvas()
    
    def OnMouseOver(self, event):
        #highlight nodes
        x = event.GetX() - self.x_shift
        y = event.GetY() - self.y_shift
        for n in self.nodes:
            if (x - n.x)**2 + (y - n.y)**2 <= (n.r+2)**2:
                n.active = True
                self.activenode = n
                self.UpdateCanvas()
            else:
                n.active = False
                
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
        
        
        
        
        
        
