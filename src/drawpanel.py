#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# drawpanel.py - implementation of the drawpanel class
# 

import wx

from controller import Controller
from node import Node

GREY = (205, 205, 205)
BLACK = (0, 0, 0)

class Drawpanel(wx.Window):
    """
    Drawpanel is a custom drawing widget which serves as a canvas.
    Events are routed to the Controller class, where they are interpreted.
    Drawpanel receives from the controller (elementhandler)
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetDoubleBuffered(True)
        
        self.c = controller
        self.color = (0,0,255)
        
        #events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        
        wx.EVT_MOTION(self, self.c.OnMouseOver)
        wx.EVT_LEFT_DOWN(self, self.c.OnLeftClick)
    
    def OnPaint(self, event=None):
        #draw buffer to the screen
        dc = wx.BufferedPaintDC(self, self._Buffer)


    def OnSize(self, event=None):
        size  = self.ClientSize
        self._Buffer = wx.EmptyBitmap(*size)
        self.UpdateDrawing()
     
    def UpdateDrawing(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        del dc # 
        self.Refresh()
        self.Update()
        
    def Draw(self, dc):
        #actual drawing code
        dc.Clear()
        dc.SetBrush(wx.Brush("white")) 
        dc.SetPen(wx.Pen("black", width=1) )
    
        self.DrawNodes(dc, self.c.grid.x, self.c.grid.y)
        s = self.c.grid.ndist
        x = self.c.grid.x
        y = self.c.grid.y
       
        
        #draw active
        self.color = GREY
        if self.c.toDraw == 'wire' and self.c.grid.ln is not None and self.c.grid.an is not None:
            dc.SetPen(wx.Pen(GREY, width=1) )
            dc.DrawLine(self.c.grid.ln.x * s + x, self.c.grid.ln.y* s + y, self.c.grid.an.x * s + x, self.c.grid.an.y * s + y)
        elif self.c.toDraw == 'resistor' and self.c.grid.an is not None:
            self.DrawElement(dc, 'resistor',  self.c.toDrawOption, self.c.grid.an.x, self.c.grid.an.y, self.c.grid.ndist)
        elif self.c.toDraw == 'voltsrc' and self.c.grid.an is not None:
            self.DrawElement(dc, 'voltsrc',  self.c.toDrawOption, self.c.grid.an.x, self.c.grid.an.y, self.c.grid.ndist)
        
        self.color = BLACK
        for e in self.c.t.elements:
            if e.name == 'wire':
                self.DrawWire(dc, e.x, e.y, e.x2, e.y2, self.c.grid.ndist)
            else:
                self.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.grid.ndist)
            
    def DrawWire(self, dc, x1, y1, x2, y2, s):
        #mh...
        dc.SetPen(wx.Pen(self.color, width=1) ) #constant sucks.
        x1 = x1*s + self.c.grid.x
        y1 = y1*s + self.c.grid.y
        x2 = x2*s + self.c.grid.x
        y2 = y2*s + self.c.grid.y
        dc.DrawLine(x1, y1, x2, y2)
    
    def DrawElement(self, dc, name, option, x, y, s):
              
        dlist = self.c.ehandler.GetDrawlist(name, option)
        x = x * s + self.c.grid.x
        y = y * s + self.c.grid.y 
        
        for d in dlist:
            if d[0] == 'line':
                dc.SetPen(wx.Pen(self.color, width=d[5]) )
                dc.DrawLine(x + d[1] * s, y + d[2]* s, x + d[3] *s, y + d[4]*s)
            elif d[0] == 'rect':
                dc.SetPen(wx.Pen(self.color, width=d[5]) )
                dc.DrawRectangle(x+d[1]*s, y +d[2]*s  , d[3]*s, d[4]*s)
            elif d[0] == 'circ':
                dc.SetPen(wx.Pen(self.color, width=d[4]) )
                dc.DrawCircle(x+d[1]*s, y +d[2]*s , d[3]*s)
            else:
                print 'unknown drawdirective...'
        
        
    
    def DrawNodes(self, dc, x, y):
        dc.SetPen(wx.Pen("grey", width=1) )
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        s = self.c.grid.ndist
        dc.SetPen(wx.Pen("black", width=1) )
        for n in  self.c.grid.nodes:
            #dc.DrawCircle( x + n.x * s, y + n.y*s, 1)
            dc.DrawPoint( x + n.x * s, y + n.y*s)
        #dc.SetPen(wx.Pen("black", width=2) )
        a = self.c.grid.an
        if a:
            dc.DrawCircle( x + a.x * s, y + a.y*s, 3)
        #if self.c.grid.ln: #debug
        #    dc.DrawCircle( x + self.c.grid.ln.x * s, y + self.c.grid.ln.y*s, 2)
                

    
    
    
    
    
