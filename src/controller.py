#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Texwizard
from elementhandler import Elementhandler
from settings import Settings
from artist import Artist

from element import Element
from grid import Grid
from node import Node
from geometry import Rectangle
            
import wx

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
        self.settings = Settings()
        self.t = Texwizard(self)
        self.grid = Grid(x_size=30, y_size=30, nodedistance=13, x=20, y=20)
        self.artist = Artist(self)
        
        #link
        self.main = main
        
        self.log = []
        
        #vars 
        self.leftdown = False
        
        #init
        self.ehandler.Readfile('resistor') #nach handler verschieben?!
        self.ehandler.Readfile('voltsrc')
        self.ehandler.Readfile('capacitor')
        self.ehandler.Readfile('currsrc')

        self.toDraw = None
        self.toDrawOption = None
        
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
        
        if self.toDraw is None:
            return
        
        if self.toDraw == 'wire': #drawing with 2 clicks
            if self.grid.ln is not None:
                self.elements.append(Element('wire', '', ln.x, ln.y, an.x, an.y ))
                self.grid.ln = None
            else:
                self.grid.ln = Node(an.x, an.y)    
        else:
            dl = self.ehandler.GetDrawlist(self.toDraw, self.toDrawOption)   
            
            box = Rectangle(self.grid.an.x+dl[-1][1], an.y+ dl[-1][2], dl[-1][3], dl[-1][4])
            #print 'x = '+str(box.x) + ', y='+str(box.y)+ ', w='+str(box.w)+ ', h='+str(box.h) 
            self.elements.append(Element(self.toDraw, self.toDrawOption, an.x, an.y, bbox=box))
        
        self.UpdateCanvas()
        
    def OnRightClick(self, event):
        if self.toDraw is not None:
            self.toDraw = None
            self.grid.ln = None
            self.main.preview.UpdateDrawing()
            return

        for e in self.elements:
            if e.bbox is not None:
                if self.IsInBoundingBox(event.GetX(), event.GetY(), e.bbox):
                    e.selected = not e.selected
                    self.UpdateCanvas()
        

    def IsInBoundingBox(self, x, y, bbox):
        b = bbox
        x = x - self.grid.x
        y = y - self.grid.y
        s = self.grid.ndist
        if b.x * s < x and (b.x + b.w )* s > x and y > b.y * s and y < (b.y+b.h) * s:
            return True
        return False
    

        
    def OnMouseOver(self, event):
        if self.grid.findActiveNode(event.GetX(), event.GetY()):
            self.UpdateCanvas()
            
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self.main, 'CIRC \n a GUI frontend for circdia.sty\t\n' '2011-\t', 'About',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                   
    def OnKeyDown(self, event):
        print 'keydown'
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            print 'deletekey'
            self.DeleteSelectedElements()
        
    def OnWriteCodeToFile(self, event):
        print self.t.GenerateCode()
        self.t.PrintToFile('test.tex')

    def OnToggleBoundingBox(self, event):
        self.settings.drawboundingbox = not self.settings.drawboundingbox 
    
    def DeleteSelectedElements(self, event=None):
        new = []
        for e in self.elements:
            if not e.selected:
                new.append(e)
        self.elements = new
        self.UpdateCanvas()
    
    def OnRemoveLast(self, event=None):
        if len(self.elements) > 0:
            self.elements.pop()
        self.UpdateCanvas()
    
    def UpdateSize(self, event):
        size = event.GetSize()
        w = size[0]
        h = size[1]
        w_b = w - self.grid.ndist * self.grid.x_size
        w_h = h - self.grid.ndist * self.grid.y_size
        if w_b/2 > 0:
            self.grid.x = w_b/2
        if w_h/2 > 0:
            self.grid.y = w_h/2
    
    def DrawWire(self, event):
        if self.toDraw is 'wire':
            self.toDraw = None
        else:
            self.toDraw = 'wire'
        self.main.preview.UpdateDrawing()
        
    def DrawResistorH(self, event):
        self.toDraw = 'resistor'
        self.toDrawOption = 'H'
        self.main.preview.UpdateDrawing()

    def DrawResistorV(self, event):
        self.toDraw = 'resistor'
        self.toDrawOption = 'V'
        self.main.preview.UpdateDrawing()
        
    def DrawVoltSrcH(self, event):
        self.toDraw = 'voltsrc'
        self.toDrawOption = 'H'
        self.main.preview.UpdateDrawing()
        
    def DrawVoltSrcV(self, event):
        self.toDraw = 'voltsrc'
        self.toDrawOption = 'V'
        self.main.preview.UpdateDrawing()
    
    def DrawCapacitor(self, event):
        self.toDraw = 'capacitor'
        if self.toDrawOption is not 'H':
            self.toDrawOption = 'H'
        else:
            self.toDrawOption = 'V'
        self.main.preview.UpdateDrawing()
    
    def DrawCurrSrc(self, event):
        self.toDraw = 'currsrc'
        if self.toDrawOption is not 'H':
            self.toDrawOption = 'H'
        else:
            self.toDrawOption = 'V'
        self.main.preview.UpdateDrawing()
        
    def UpdateCanvas(self):
        self.main.drawpanel.UpdateDrawing()
        
        
        
        
        
        
        
