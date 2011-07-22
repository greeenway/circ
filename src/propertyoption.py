#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# propertyoption.py 
# 

import wx

class Propertyoption:
    def __init__(self, parent, sizer, controller, name, type='TEXT', list=[]):
        self.parent = parent
        self.sizer = sizer
        self.c = controller
        self.name = name
        self.type = type
        self.list = list
        self.label = wx.StaticText(self.parent, label=self.name, style=wx.ALIGN_LEFT)
        
        if self.type is 'TEXT':
            self.input = wx.TextCtrl(self.parent, value='')
            self.input.Bind(wx.EVT_TEXT, self.OnHandleEvent)

        else:
            self.input = wx.ComboBox(self.parent, value=list[0],
                                     choices=list)
            self.input.Bind(wx.EVT_COMBOBOX, self.OnHandleEvent)
        
        self.sizer.Add(self.label, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.input, 1, wx.EXPAND | wx.ALL)        
        
    def OnHandleEvent(self, event=None):
        #print 'name = ' + str(self.name)
        #print 'input = ' + self.input.GetValue()
        self.c.SetOption(self.name, self.input.GetValue())
        self.c.UpdateCanvas()