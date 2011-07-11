#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Texwizard
from elementhandler import Elementhandler

from element import Element
from grid import Grid
from node import Node
            
import time

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
        self.grid = Grid(x_size=30, y_size=30, nodedistance=13, x=20, y=20)
        #link
        self.main = main
        
        self.log = []
        
        #vars 
        self.leftdown = False
        
        #init
        self.ehandler.Readfile('resistor') #nach handler verschieben?!
        self.ehandler.Readfile('voltsrc')

        self.toDraw = 'resistor'
        self.toDrawOption = 'H'
        
    def PrintLog(self):
        res = ''
        for entry in self.log:
            res += entry
            res += '\n'
        return res
    
    def OnLeftClick(self, event):
        an = self.grid.an
        ln = self.grid.ln
        if an == None:
            return

        if self.toDraw == 'wire': #drawing with 2 clicks
            if self.grid.ln is not None:
                self.elements.append(Element('wire', '', ln.x, ln.y, an.x, an.y ))
                self.grid.ln = None
            else:
                self.grid.ln = Node(an.x, an.y)    
        else:
            self.elements.append(Element(self.toDraw, self.toDrawOption, an.x, an.y))
        self.UpdateCanvas()
        pass

    
    def OnMouseOver(self, event):
        if self.grid.findActiveNode(event.GetX(), event.GetY()):
            self.UpdateCanvas()
        
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
        
    def DrawVoltSrcH(self, event):
        self.toDraw = 'voltsrc'
        self.toDrawOption = 'H'
        
    def DrawVoltSrcV(self, event):
        self.toDraw = 'voltsrc'
        self.toDrawOption = 'V'
    
    def UpdateCanvas(self):
        self.main.drawpanel.UpdateDrawing()
        
        
        
        
        
        
