#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main.py - executable file of the project
# 

#TODO
# filled rects todo
# implement drawing code for circles


import wx
from drawpanel import Drawpanel
from controller import Controller
from texwizard import Texwizard

ID_SHOW_LOG = wx.NewId()

class Mainwindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600,500))
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', 'Some Information.')
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program')
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnClose)
        
        #DEBUG
        debugmenu = wx.Menu()
        debugmenu.Append(ID_SHOW_LOG, 'Show &Log', 'Show Controller\'s Log')
        wx.EVT_MENU(self, ID_SHOW_LOG, self.OnShowLog)
        
        self.texwizard = Texwizard()
        self.controller = Controller(self, self.texwizard) # controller!
        self.drawpanel = Drawpanel(self, self.controller)
        self.buttons = []
        
        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bhsizer = wx.BoxSizer(wx.VERTICAL)
        
        self.wirebutton = wx.Button(self, -1, 'Draw wire')
        self.wirebutton.Bind(wx.EVT_BUTTON, self.controller.DrawWire)
        self.resistorHbutton = wx.Button(self, -1, 'Draw R(H)')
        self.resistorHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorH)
        self.resistorVbutton = wx.Button(self, -1, 'Draw R(V)')
        self.resistorVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorV)
        
        self.bhsizer.Add(self.wirebutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorHbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorVbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        
        for i in range(0, 4):
            self.buttons.append(wx.Button(self, -1, 'button ' + str(i)))
            self.bhsizer.Add(self.buttons[i], 1, wx.EXPAND | wx.BOTTOM, border=2)
            
        self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        self.vsizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=3)

        
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        #self.vsizer.Fit(self)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        menubar.Append(debugmenu, '&Debug')
        self.SetMenuBar(menubar)
        self.Show(True)
    
    def OnShowLog(self, event):
        print self.controller.PrintLog()
    
    def OnClose(self, event):
        self.Close()
        

if __name__ == '__main__':        
    app = wx.App(False)
    frame = Mainwindow(None, 'CIRC')
    frame.Show()
    app.MainLoop()

