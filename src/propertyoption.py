#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# propertyoption.py 
# 

import wx

class Propertyoption:
    """Handles a static text and an option, routes events to the controller"""
    def __init__(self, parent, sizer, controller, name, type='TEXT', list=[],
                 defaultvalue = ''):
        self.parent = parent
        self.sizer = sizer
        self.c = controller
        self.name = name
        self.type = type
        self.list = list
        self.value = ''
        self.label = wx.StaticText(self.parent, label=self.name, style=wx.ALIGN_LEFT)
        
        if self.type is 'TEXT':
            self.input = wx.TextCtrl(self.parent, value=defaultvalue)
            self.input.Bind(wx.EVT_TEXT, self.OnHandleEvent)

        else:
            self.input = wx.ComboBox(self.parent, value=list[0],
                                     choices=list, style=wx.CB_READONLY)
            self.input.Bind(wx.EVT_COMBOBOX, self.OnHandleEvent)
        
        self.sizer.Add(self.label, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.input, 2, wx.EXPAND | wx.ALL)        
    
    def ChangeProperty(self, name, value):
        #print 'changing property'
        if self.type is 'LIST':
            index = -1
            for i,n in enumerate(self.list):
                if n == value:
                    index = i
            if index >= 0:
                self.input.SetSelection(index)
                self.value = value
        else:
            self.input.SetValue(value)
            self.value = value
            
    
    def OnHandleEvent(self, event=None):
        self.value = self.input.GetValue()
        self.c.SetOption(self.name, self.input.GetValue())
        if self.name == 'Orientation':
            
            self.c.curPattern.ChangeOrientation(str(self.input.GetValue()))
            self.c.main.configpanel.update_properties()
            
        
        
        