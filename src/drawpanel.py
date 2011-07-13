#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# drawpanel.py - implementation of the drawpanel class
# 

import wx

from controller import Controller
from node import Node

GREY = (205, 205, 205)
BLACK = (0, 0, 0)
LIGHTBLUE = (0, 0, 255)
SELECTED = (255, 204, 0)

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
        
        #make events local?
        wx.EVT_MOTION(self, self.c.OnMouseOver)
        wx.EVT_LEFT_DOWN(self, self.c.OnLeftClick)
        wx.EVT_RIGHT_DOWN(self, self.c.OnRightClick)
        wx.EVT_KEY_DOWN(self, self.c.OnKeyDown)
    
    def OnPaint(self, event=None):
        #draw buffer to the screen
        dc = wx.BufferedPaintDC(self, self._Buffer)


    def OnSize(self, event=None):
        size  = self.ClientSize
        self._Buffer = wx.EmptyBitmap(*size)
        self.UpdateDrawing()
        self.c.UpdateSize(event)
        
     
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
       
        #dc.DrawLabel('Hallo Welt', wx.Rect(40,40, 50, 20), alignment= wx.ALIGN_LEFT)
        #dc.DrawTextPoint('Hallo Welt', wx.Point(40,40))
        
        for e in self.c.elements:
            self.color = BLACK
            if e.name == 'wire':
                self.DrawWire(dc, e.x, e.y, e.x2, e.y2, self.c.grid.ndist)
            else:
                if e.selected:
                    self.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.grid.ndist, 
                                 self.c.settings.drawboundingbox,
                                 selected = True)
                else:
                    self.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.grid.ndist, 
                                 self.c.settings.drawboundingbox)
        
        #draw active
        self.color = GREY
        if self.c.toDraw is not None and self.c.grid.an is not None:
            if self.c.toDraw == 'wire' and self.c.grid.ln is not None and self.c.grid.an is not None:
                dc.SetPen(wx.Pen(GREY, width=1) )
                dc.DrawLine(self.c.grid.ln.x * s + x, self.c.grid.ln.y* s + y, self.c.grid.an.x * s + x, self.c.grid.an.y * s + y)
            elif self.c.toDraw is not 'wire':
                self.DrawElement(dc, self.c.toDraw,  self.c.toDrawOption, self.c.grid.an.x, self.c.grid.an.y, self.c.grid.ndist)
           
        
    
            
    def DrawWire(self, dc, x1, y1, x2, y2, s):
        #mh...
        dc.SetPen(wx.Pen(self.color, width=1) ) #constant sucks.
        x1 = x1*s + self.c.grid.x
        y1 = y1*s + self.c.grid.y
        x2 = x2*s + self.c.grid.x
        y2 = y2*s + self.c.grid.y
        dc.DrawLine(x1, y1, x2, y2)
    
    def DrawElement(self, dc, name, option, x, y, s, bbox = False, selected = False):
              
        dlist = self.c.ehandler.GetDrawlist(name, option)
        x = x * s + self.c.grid.x
        y = y * s + self.c.grid.y 
        
        #the asymmetric resistor (rect) problem:
        #it is needed to add linewidth to the rect-width
        #despite this the value 1.88 seems to leads to some rounding errors,
        #eg. 2.0 produces a totally symmetric result
        thick = 0
        oldcolor = self.color
        
        for d in dlist:
            for i in range(2):
                if selected:
                    if i is 0:
                        thick = 5
                        self.color = SELECTED
                    else:
                        thick = 0
                        self.color = oldcolor
            
                if d[0] == 'line':
                    dc.SetPen(wx.Pen(self.color, width=d[5]+thick) )
                    dc.DrawLine(x + d[1] * s, y + d[2]* s, x + d[3] *s, y + d[4]*s)
                elif d[0] == 'rect':
                    dc.SetPen(wx.Pen(self.color, width=d[5]+thick) )
                    dc.DrawRectangle(x+d[1]*s, y +d[2]*s  , d[3]*s+1*d[5], d[4]*s+1*d[5]) 
                elif d[0] == 'circ':
                    dc.SetPen(wx.Pen(self.color, width=d[4]+thick) )
                    dc.DrawCircle(x+d[1]*s, y +d[2]*s , d[3]*s)
                elif d[0] == 'bbox' and bbox:
                    dc.SetPen(wx.Pen(LIGHTBLUE, width=1) )
                    dc.DrawRectangle(x+d[1]*s, y + d[2]*s  , d[3]*s+1, d[4]*s+1)

        
        
    
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
                

    
    
    
    
    
