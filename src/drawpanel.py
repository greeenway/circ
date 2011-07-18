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
        self.Bind(wx.EVT_LEFT_UP, self.c.OnLeftUp)
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
        #font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        #dc.SetFont(font1)
        #dc.DrawTextPoint('Hallo Welt! 123456789', wx.Point(40,40))
        
        for e in self.c.elements:
            self.c.artist.color = BLACK
            self.c.artist.DrawElement(dc, e)

        #draw active
        self.c.artist.color = GREY
        if self.c.curPattern is not None and self.c.grid.an is not None:
            if self.c.curPattern.special is 'wire':
                if self.c.grid.ln is not None and self.c.grid.an is not None:
                    self.c.curPattern.sample.x = self.c.grid.ln.x
                    self.c.curPattern.sample.y = self.c.grid.ln.y
                    self.c.curPattern.sample.x2 = self.c.grid.an.x
                    self.c.curPattern.sample.y2 = self.c.grid.an.y
                    self.c.artist.DrawElement(dc, self.c.curPattern.sample)
                    
            else:
                self.c.curPattern.sample.x = self.c.grid.an.x #wire to do
                self.c.curPattern.sample.y = self.c.grid.an.y
                self.c.artist.DrawElement(dc, self.c.curPattern.sample)

           

    
    
    
    
    
