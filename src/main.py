#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main.py - executable file of the project
# 

#TODO
# filled rects todo
# implement drawing code for circles
# rect asymmetric...
# invert coordinate system
# improve codegeneration code
# collision detection
# add text to elements.

import wx
from drawpanel import Drawpanel
from controller import Controller
from texwizard import Texwizard

ID_SHOW_LOG = wx.NewId()
ID_WRITE_TEX_TO_FILE = wx.NewId()
ID_TOGGLE_BBOX = wx.NewId()
ID_REMOVE_SELECTED = wx.NewId()
ID_REMOVE_LAST = wx.NewId()

class Mainwindow(wx.Frame):
    """
    Mainwindow is the main class for the GUI. 
    Beside of providing a home for Controller and Drawpanel, it
    also defines the GUI and routes Events.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600,500))
        
        self.controller = Controller(self) 
        self.drawpanel = Drawpanel(self, self.controller)

        self.CreateStatusBar()
        
        # ------------------------- create menue ------------------------------------------
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', 'Some Information.')
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program')
        
        
        buildmenu = wx.Menu()
        buildmenu.Append(ID_WRITE_TEX_TO_FILE, '&Write Code', 'Generate LaTeX-Output (fileoutput).')
        
        editmenu = wx.Menu()
        editmenu.Append(ID_REMOVE_SELECTED, '&Remove selected Elements', 'Remove all selected elements.')
        editmenu.Append(ID_REMOVE_LAST, '&Remove last Element', 'Remove the last created object.')
        
        # event routing
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnClose)
        wx.EVT_MENU(self, ID_WRITE_TEX_TO_FILE, self.controller.OnWriteCodeToFile) 
        wx.EVT_MENU(self, ID_REMOVE_SELECTED, self.controller.DeleteSelectedElements)
        wx.EVT_MENU(self, ID_REMOVE_LAST, self.controller.OnRemoveLast)
        
        #DEBUG
        debugmenu = wx.Menu()
        debugmenu.Append(ID_SHOW_LOG, 'Show &Log', 'Show Controller\'s Log')
        debugmenu.Append(ID_TOGGLE_BBOX, '&Toggle Visibility of BoundingBoxes')
        wx.EVT_MENU(self, ID_SHOW_LOG, self.OnShowLog) #move to controller?
        wx.EVT_MENU(self, ID_TOGGLE_BBOX, self.controller.OnToggleBoundingBox)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        menubar.Append(editmenu, '&Edit')
        menubar.Append(buildmenu, '&Build')
        menubar.Append(debugmenu, '&Debug')
        self.SetMenuBar(menubar)
        # ------------------------- / create menue ------------------------------------------
        
        # ---------------------- buttons --------------------------------------------- 
        self.buttons = []

        self.wirebutton = wx.Button(self, -1, 'wire')  
        self.resistorHbutton = wx.Button(self, -1, 'R(H)')
        self.resistorVbutton = wx.Button(self, -1, 'R(V)')
        self.vltsrcHbutton = wx.Button(self, -1, 'VSrc(H)')
        self.vltsrcVbutton = wx.Button(self, -1, 'VSrc(V)')
        self.capacitorButton = wx.Button(self, -1, 'C')
        
        # event routing
        self.wirebutton.Bind(wx.EVT_BUTTON, self.controller.DrawWire)
        self.resistorHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorH)
        self.resistorVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorV)
        self.vltsrcHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcH)
        self.vltsrcVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcV)
        self.capacitorButton.Bind(wx.EVT_BUTTON, self.controller.DrawCapacitor)
        
        # ---------------------- / buttons --------------------------------------------- 
        
        # ----------------------- sizers -----------------------------------------------
        self.vsizer = wx.BoxSizer(wx.HORIZONTAL) 
        self.bhsizer = wx.BoxSizer(wx.VERTICAL)  
        
        self.bhsizer.Add(self.wirebutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorHbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorVbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.vltsrcHbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.vltsrcVbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.capacitorButton, 1, wx.EXPAND | wx.BOTTOM, border=2)
            
        self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        self.vsizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=3)

        
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        # ----------------------- / sizers -----------------------------------------------
        
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

