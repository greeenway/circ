#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Element

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
        self.x_shift = 0#10
        self.y_shift = 0#10 
        
        self.nodes = []
        j = 1
        for i in range(1,400):
            self.nodes.append(Node((i % 20) * 15 + 15, j * 15 + 15, 3))
            if i % 20 == 0:
                j += 1
        
    def PrintLog(self):
        res = ''
        for entry in self.log:
            res += entry
            res += '\n'
        return res
    
    def OnLeftClick(self, event):
        #print 'leftclick'
        self.t.elements.append(Element('R', event.GetX(), event.GetY()))
        self.UpdateCanvas()
    
    def OnMouseOver(self, event):
        #highlight nodes
        x = event.GetX() #+ self.x_shift
        y = event.GetY() + self.y_shift
        for n in self.nodes:
            if (x - n.x)**2 + (y - n.y)**2 <= (n.r+2)**2:
                n.active = True
                self.UpdateCanvas()
            else:
                n.active = False
        
    
    def UpdateCanvas(self):
        self.main.drawpanel.UpdateDrawing()
        
        
        
        
        
        