#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# drawpanel.py - implementation of the drawpanel class
# 

import wx

from controller import Controller
from controller import Node

class Drawpanel(wx.Window):
    """
    Drawpanel is a custom drawing widget which serves as a canvas.
    Events are routed to the Controller class, where they are interpreted.
    Drawpanel receives from the controller (elementhandler)
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.c = controller
        
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
    
        self.DrawNodes(dc, self.c.x_shift, self.c.y_shift, self.c.nodes)
        
        for e in self.c.t.elements:
            if e.name == 'wire':
                self.DrawWire(dc, e.x, e.y, e.x2, e.y2, self.c.gridsize)
            else:
                self.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.gridsize)
            
    def DrawWire(self, dc, x1, y1, x2, y2, s):
        #mh...
        dc.SetPen(wx.Pen("black", width=1) ) #constant sucks.
        x1 = x1*s + self.c.x_shift
        y1 = y1*s + self.c.y_shift
        x2 = x2*s + self.c.x_shift
        y2 = y2*s + self.c.y_shift
        dc.DrawLine(x1, y1, x2, y2)
    
    def DrawElement(self, dc, name, option, x, y, s):
              
        dlist = self.c.ehandler.GetDrawlist(name, option)
        x = x * s + self.c.x_shift
        y = y * s + self.c.y_shift 
        
        for d in dlist:
            if d[0] == 'line':
                dc.SetPen(wx.Pen("black", width=d[5]) )
                dc.DrawLine(x + d[1] * s, y + d[2]* s, x + d[3] *s, y + d[4]*s)
            elif d[0] == 'rect':
                dc.SetPen(wx.Pen("black", width=d[5]) )
                dc.DrawRectangle(x+d[1]*s, y +d[2]*s  , d[3]*s, d[4]*s)
            elif d[0] == 'circ':
                pass
            else:
                print 'unknown drawdirective...'
        
        
    
    def DrawNodes(self, dc, x, y, nodes):
        dc.SetPen(wx.Pen("grey", width=1) )
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        s = self.c.gridsize
        for n in nodes:
            if n.active:
                dc.SetPen(wx.Pen("black", width=2) )
                #dc.SetBrush(wx.Brush(wx.Colour(0,255,0)))
            else:
                dc.SetPen(wx.Pen("grey", width=1) )
                #dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
            dc.DrawCircle( x + n.x * s, y + n.y*s, n.r)
    
