#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# preview.py - implementation of the preview class
# 

import wx

from controller import Controller

GREY = (205, 205, 205)
BLACK = (0, 0, 0)
WIDTH = 200
HEIGHT = 150

class Preview(wx.Window):
    """
    Preview renders a preview of the Elements
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.BORDER_RAISED,
                           size=wx.Size(WIDTH,HEIGHT))
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

        font1 = wx.Font(13, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        dc.SetFont(font1)

        if self.c.curPattern is not None:
            self.c.artist.DrawElement(dc, self.c.curPattern.sample,
                    preview = True, px = WIDTH/2 , py = HEIGHT/2, ps = WIDTH/12)
            

           
        


