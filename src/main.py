#!/usr/bin/env python
# a hello world example from wikipedia.org

import wx
 
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        
        filemenu.Append(wx.ID_ABOUT, "&About", "Some Information.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)
        
        
 
app = wx.App(False)
frame = MainWindow(None, "circ")
frame.Show()
app.MainLoop()

