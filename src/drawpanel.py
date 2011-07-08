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
        try:
            self.bmp1 = wx.Image('../files/images/R.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        except IOError:
            print 'no image found.'
    
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
        self.c.log.append('Click at (' + str(event.GetX()) + '/' + str(event.GetX()) + ')')
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
            dc.DrawBitmap(self.bmp1, e.x, e.y)

    def DrawNodes(self, dc, x, y, nodes):
        dc.SetPen(wx.Pen("black", width=1) )
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        for n in nodes:
            if n.active:
                dc.SetPen(wx.Pen("black", width=2) )
                #dc.SetBrush(wx.Brush(wx.Colour(0,255,0)))
            else:
                dc.SetPen(wx.Pen("black", width=1) )
                #dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
            dc.DrawCircle( x + n.x, y + n.y, n.r)
    
    def DrawGrid(self, dc, width, height, delta=15):
        x = delta
        y = delta
        while x < width:
            while y < height:
                dc.DrawCircle(x, y, 2)
                y = y + delta
            y = delta
            x = x + delta