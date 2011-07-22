#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# settingsframe.py - implementation of the Settingsframe class
# 

import wx

TITLE = 'Settings'
SIZE = (300,300)

class Settingsframe(wx.Frame):
    """Lets the user change settings of the application"""
    def __init__(self, parent, controller):
        wx.Frame.__init__(self, parent, title=TITLE, size=SIZE
                          )
        self.c = controller
        self.xSliderLabel = wx.StaticText(self, label='x_size:')
        self.xSlider = wx.Slider(self, value=self.c.grid.x_size, minValue=10,
                                 maxValue=100)
        
        self.ySliderLabel = wx.StaticText(self, label='y_size:')
        self.ySlider = wx.Slider(self, value=self.c.grid.y_size, minValue=10,
                                 maxValue=100, 
                                 style= wx.SL_AUTOTICKS | wx.SL_LABELS)
        #eventrouting
        self.xSlider.Bind(wx.EVT_SCROLL, self.OnXScroll)
        self.ySlider.Bind(wx.EVT_SCROLL, self.OnYScroll)
        
        #sizers
        self.xslidersizer = wx.BoxSizer(wx.HORIZONTAL)
        self.yslidersizer = wx.BoxSizer(wx.HORIZONTAL)
        self.xslidersizer.Add(self.xSliderLabel, 1, wx.EXPAND | wx.ALL, border=5)
        self.xslidersizer.Add(self.xSlider, 1, wx.EXPAND | wx.ALL, border=5)
        self.yslidersizer.Add(self.ySliderLabel, 1, wx.EXPAND | wx.ALL, border=5)
        self.yslidersizer.Add(self.ySlider, 1, wx.EXPAND | wx.ALL, border=5)
        
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainsizer.Add(self.xslidersizer, 0, wx.EXPAND | wx.ALL, border=5)
        self.mainsizer.Add(self.yslidersizer, 0, wx.EXPAND | wx.ALL, border=5)
        
        self.SetSizer(self.mainsizer)
        self.SetAutoLayout(1)
        self.Show(True)
    
    #handlers
    def OnXScroll(self, event):
        self.c.grid.changeNodes(event.GetPosition(), 
                                self.c.grid.y_size, self.c.grid.ndist)
        self.c.UpdateSize()
        self.c.UpdateCanvas()
    
    
    def OnYScroll(self, event):
        self.c.grid.changeNodes(self.c.grid.x_size,
                                event.GetPosition(), self.c.grid.ndist)
        self.c.UpdateSize()
        self.c.UpdateCanvas()