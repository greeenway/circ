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
        self.curPattern = None
        self.mode = 'SELECT'
        
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
        self.ehandler.Readfile('inductor')
        
        #self.toDraw = None
        #self.toDrawOption = None
        
    def PrintLog(self):
        res = ''
        for entry in self.log:
            res += entry
            res += '\n'
        return res
        
    def OnRotate(self, event=None):
        if self.curPattern:
            self.curPattern.sample.Rotate()
            self.curPattern.Rotate()
        
        for e in self.elements:
            if e.selected:
                e.Rotate()
        self.UpdateCanvas()
        
        
    
    def OnLeftClick(self, event):
        an = self.grid.an
        ln = self.grid.ln
        if an == None:
            return
        if self.mode == 'INSERT':
            if self.curPattern is not None:
                if self.curPattern.special is None:
                    elem = self.curPattern.CreateElement(an.x, an.y, x2 = 0, y2 = 0)
                    #if self.elements:
                    #    self.elements[-1].selected = False
                    #elem.selected = True
                    self.elements.append(elem)
                    
                if self.curPattern.special is 'wire':
                    if ln is None:
                        self.grid.ln = an
        elif self.mode == 'SELECT':
            for e in self.elements:
                if e.bbox is not None:
                    if self.IsInBoundingBox(event.GetX(), event.GetY(), e.bbox):
                        e.selected = not e.selected
        self.UpdateCanvas()
        
    def OnLeftUp(self, event):
        an = self.grid.an
        ln = self.grid.ln
        
        if an == None:
            return
        if self.curPattern is not None:
            if self.curPattern.special is 'wire':
                if ln is not None:
                    elem = self.curPattern.CreateElement(ln.x, ln.y, an.x, an.y)
                    self.elements.append(elem)
                    self.grid.ln = None
                    self.UpdateCanvas()
                
                
        
    def OnRightClick(self, event):
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
    
    def OnSelect(self, event=None):
        self.mode = 'SELECT'
        
    def OnWriteCodeToFile(self, event):
        print self.t.GenerateCode()
        self.t.PrintToFile('test.tex')

    def OnToggleBoundingBox(self, event):
        self.settings.drawboundingbox = not self.settings.drawboundingbox 
        self.UpdateCanvas()
    
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
    
    def DrawWire(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].wirePattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    def DrawResistor(self, event= None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].resistorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
    
    def DrawInductor(self, event=None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].inductorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    def DrawVoltSrc(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].vltsrcPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    
    def DrawCapacitor(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].capacitorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
    
    def DrawCurrSrc(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].cursrcPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    def UpdateCanvas(self):
        
        self.main.drawpanel.UpdateDrawing()
        
        #maybe optimize this:
        self.main.pages[self.main.activePage].preview.UpdateDrawing()
        
        
        
        
        
        
        
