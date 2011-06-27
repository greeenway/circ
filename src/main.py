#!/usr/bin/env python
# a hello world example from wikipedia.org

import wx
 
class TestFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        text = wx.StaticText(self, label="Hello, World!")
 
app = wx.App(redirect=False)
frame = TestFrame(None, "Hello, world!")
frame.Show()
app.MainLoop()

