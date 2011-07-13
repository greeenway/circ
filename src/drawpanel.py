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
        #wx.EVT_KEY_DOWN(self, self.c.OnKeyDown)
    
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
    
        self.c.artist.DrawNodes(dc, self.c.grid.x, self.c.grid.y)
        s = self.c.grid.ndist
        x = self.c.grid.x
        y = self.c.grid.y
       
        #dc.DrawLabel('Hallo Welt', wx.Rect(40,40, 50, 20), alignment= wx.ALIGN_LEFT)
        font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        dc.SetFont(font1)
        #dc.DrawTextPoint('Hallo Welt! 123456789', wx.Point(40,40))
        for e in self.c.elements:
            self.c.artist.color = BLACK
            if e.name == 'wire':
                self.c.artist.DrawWire(dc, e.x, e.y, e.x2, e.y2, self.c.grid.ndist)
            else:
                if e.selected:
                    self.c.artist.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.grid.ndist, 
                                 self.c.settings.drawboundingbox,
                                 selected = True)
                else:
                    self.c.artist.DrawElement(dc, e.name, e.option, e.x, e.y, self.c.grid.ndist, 
                                 self.c.settings.drawboundingbox)
        
        #draw active
        self.c.artist.color = GREY
        if self.c.toDraw is not None and self.c.grid.an is not None:
            if self.c.toDraw == 'wire' and self.c.grid.ln is not None and self.c.grid.an is not None:
                dc.SetPen(wx.Pen(GREY, width=1) )
                dc.DrawLine(self.c.grid.ln.x * s + x, self.c.grid.ln.y* s + y, self.c.grid.an.x * s + x, self.c.grid.an.y * s + y)
            elif self.c.toDraw is not 'wire':
                self.c.artist.DrawElement(dc, self.c.toDraw,  self.c.toDrawOption, self.c.grid.an.x, self.c.grid.an.y, self.c.grid.ndist)
           

    
    
    
    
    
