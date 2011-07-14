#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# elementlist.py - implementation of the preview Elementlist
# 
# NOT USED ATM

import wx

from controller import Controller
from geometry import Rectangle

GREY = (205, 205, 205)
LIGHT_GREY = (235, 235, 235)
BLACK = (0, 0, 0)
SELECTED = (255, 204, 0)

WIDTH = 150
HEIGHT = 400

ACTIVE = 0
VISIBLE = 1
HIDDEN = 2

class Elementlist(wx.Window):
    """
    Preview renders a preview of the Elements
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE, size=wx.Size(WIDTH,HEIGHT))
        self.SetDoubleBuffered(True)
        self.parent = parent
        self.c = controller
        self.color = (0,0,255)
        self.elements = []
        self.activeText = ''
        self.elements = ['wire']
        for e in self.c.ehandler.elements:
            for o in e.options:
                self.elements.append(e.name + '{'+ o + '}')
        
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

        
        font1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
        selectedBrush = wx.Brush(SELECTED, wx.SOLID|wx.SOLID)
        greyBrush = wx.Brush(GREY, wx.SOLID)
        hiddenBrush = wx.Brush(LIGHT_GREY, wx.SOLID)
        
        dc.SetFont(font1)
        
        dc.SetBrush(hiddenBrush)
        
        i = 0
        for e in self.elements: #self.c.ehandler.elements:
            if e.find(self.activeText) is not -1 and len(self.activeText) > 0:
                if i is 0:
                    dc.SetBrush(selectedBrush)
                else:
                    dc.SetBrush(greyBrush)
            else:
                dc.SetBrush(hiddenBrush)

                
            dc.DrawRectangle(0, i*25, self.ClientSize[0]-2, 22)
            dc.DrawText(e, 5, i*25)
            i += 1
    
    def TextChange(self, text):
        self.activeText = text
        pre = []
        out = []
        for e in self.elements:
            if e.find(self.activeText) is not -1 and len(self.activeText) > 0:
                pre.append(e)
            else:
                out.append(e)
        
        self.elements =  pre + out
        if len(pre) > 0:
            if pre[0] is 'wire':
                self.c.toDraw = pre[0]
            else:
                self.c.toDraw = pre[0][:-3]
                self.c.toDrawOption = pre[0][-2:-1]
            self.UpdateDrawing()
            self.c.UpdateCanvas()
        
        
        
        
        
        
        
        
        
