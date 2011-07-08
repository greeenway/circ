#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main.py - executable file of the project
# 

import wx
from drawpanel import Drawpanel

class Mainwindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600,400))
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        
        filemenu.Append(wx.ID_ABOUT, "&About", "Some Information.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        self.drawpanel = Drawpanel(self)
        self.buttons = []
        
        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bhsizer = wx.BoxSizer(wx.VERTICAL)
        
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "button " + str(i)))
            self.bhsizer.Add(self.buttons[i], 1, wx.EXPAND | wx.BOTTOM, border=2)
            
        self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        self.vsizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=3)

        
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        #self.vsizer.Fit(self)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)
        

if __name__ == '__main__':        
    app = wx.App(False)
    frame = Mainwindow(None, "CIRC")
    frame.Show()
    app.MainLoop()

