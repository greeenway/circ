#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# drawpanel.py - implementation of the drawpanel class
# 

import wx

from controller import Controller
from controller import Node

class Drawpanel(wx.Window):
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.c = controller
        
        #events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_MOTION(self, self.c.OnMouseOver)
        wx.EVT_LEFT_DOWN(self, self.OnMouseClick)
        
        #loading files
        #try:
            #self.bmp1 = wx.Image('../files/images/R.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #except IOError:
        #    print 'no image found.'
    
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
        
        
    def OnMouseClick(self, event):
        self.c.log.append('Click at (' + str(event.GetX()) + '/' + str(event.GetY()) + ')')
        self.c.OnLeftClick(event)
        
    def Draw(self, dc):
        #actual drawing code
        dc.Clear()
        dc.SetBrush(wx.Brush("white"))

        
        dc.SetPen(wx.Pen("black", width=1) )
    
        #red = wx.Colour(255,0,0)
        #brush = wx.Brush(red, wx.TRANSPARENT)
        #self.DrawGrid(dc, 300, 300)
        #dc.SetBrush(brush)
        self.DrawNodes(dc, self.c.x_shift, self.c.y_shift, self.c.nodes)
        
        for e in self.c.t.elements:
            if e.name == 'wire':
                self.DrawWire(dc, e.x, e.y, e.x2, e.y2, self.c.gridsize)
            else:
                self.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.gridsize)
            
    def DrawWire(self, dc, x1, y1, x2, y2, s):
        #mh...
        dc.SetPen(wx.Pen("black", width=1) ) #constant sucks.
        x1 = x1 + self.c.x_shift
        y1 = y1 + self.c.y_shift
        x2 = x2 + self.c.x_shift
        y2 = y2 + self.c.y_shift
        dc.DrawLine(x1, y1, x2, y2)
    
    def DrawElement(self, dc, name, option, x, y, s):
              
        dlist = self.c.ehandler.GetDrawlist(name, option)
        x = x + self.c.x_shift
        y = y + self.c.y_shift
        
        
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
        for n in nodes:
            if n.active:
                dc.SetPen(wx.Pen("black", width=2) )
                #dc.SetBrush(wx.Brush(wx.Colour(0,255,0)))
            else:
                dc.SetPen(wx.Pen("grey", width=1) )
                #dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
            dc.DrawCircle( x + n.x, y + n.y, n.r)
    
