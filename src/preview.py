#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# preview.py - implementation of the preview class
# 

import wx

from controller import Controller

GREY = (205, 205, 205)
BLACK = (0, 0, 0)
WIDTH = 150
HEIGHT = 150

class Preview(wx.Window):
    """
    Preview renders a preview of the Elements
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE, size=wx.Size(WIDTH,HEIGHT))
        self.SetDoubleBuffered(True)
        
        self.c = controller
        self.color = (0,0,255)
        
        #events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
    
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
        self.c.artist.color = BLACK
        name = self.c.toDraw
        option = self.c.toDrawOption
        
        font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        dc.SetFont(font1)
        dc.DrawTextPoint(str(name), (WIDTH/4, HEIGHT*5/6))
        #dc.DrawLabel(str(name), wx.Rect(WIDTH/2, HEIGHT*5/6, WIDTH, HEIGHT/2), alignment=wx.ALIGN_TOP)
        
        if name is not None:
            if name == 'wire':
                self.c.artist.DrawWire(dc, WIDTH/5, HEIGHT*0.4, 3*WIDTH/4, HEIGHT*0.2, 1, preview = True)
            else:
                self.c.artist.DrawElement(dc, name, option, WIDTH/2, HEIGHT/2, WIDTH/12, False, preview = True)
 
    

           
        


