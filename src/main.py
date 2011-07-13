#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main.py - executable file of the project
# 

#TODO
# filled rects todo
# improve codegeneration code
# add text to elements.
# add red status bar on errors

import wx
from drawpanel import Drawpanel
from controller import Controller
from texwizard import Texwizard
from preview import Preview

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
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        
        ###
        splitter = wx.SplitterWindow(self, -1)
        propertyPanel = wx.Panel(splitter, -1, style=wx.BORDER_RAISED)
        drawingPanel = wx.Panel(splitter, -1, style=wx.BORDER_RAISED)
        ##
        
        self.controller = Controller(self) 
        self.drawpanel = Drawpanel(drawingPanel, self.controller)
        self.preview = Preview(propertyPanel, self.controller)
        self.CreateStatusBar()
        
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_VERTICAL)
        self.toolbar.AddLabelTool(ID_REMOVE_LAST, 'Back', wx.Bitmap('../files/images/back.png'))
        self.toolbar.AddLabelTool(ID_REMOVE_SELECTED, 'Delete', wx.Bitmap('../files/images/delete.png'))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.controller.OnRemoveLast, id=ID_REMOVE_LAST)
        self.Bind(wx.EVT_TOOL, self.controller.DeleteSelectedElements, id=ID_REMOVE_SELECTED)
        
        
        
        # ------------------------- create menue ------------------------------------------
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', 'Some Information.')
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program\tCtrl+Q')
        
        
        buildmenu = wx.Menu()
        buildmenu.Append(ID_WRITE_TEX_TO_FILE, '&Write Code\tCtrl+W', 'Generate LaTeX-Output (fileoutput).')
        
        editmenu = wx.Menu()
        editmenu.Append(ID_REMOVE_SELECTED, '&Remove selected Elements', 'Remove all selected elements.')
        editmenu.Append(ID_REMOVE_LAST, '&Remove last Element\tCtrl+Z', 'Remove the last created object.')
        
        # event routing
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnClose)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.controller.OnAbout)
        wx.EVT_MENU(self, ID_WRITE_TEX_TO_FILE, self.controller.OnWriteCodeToFile) 
        wx.EVT_MENU(self, ID_REMOVE_SELECTED, self.controller.DeleteSelectedElements)
        wx.EVT_MENU(self, ID_REMOVE_LAST, self.controller.OnRemoveLast)
        
        #DEBUG
        debugmenu = wx.Menu()
        debugmenu.Append(ID_SHOW_LOG, 'Show &Log', 'Show Controller\'s Log')
        debugmenu.Append(ID_TOGGLE_BBOX, '&Show BoundingBoxes', kind=wx.ITEM_CHECK)
        debugmenu.Check(ID_TOGGLE_BBOX, False)
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

        self.wirebutton = wx.Button(propertyPanel, -1, 'wire')  
        self.resistorHbutton = wx.Button(propertyPanel, -1, 'R(H)')
        self.resistorVbutton = wx.Button(propertyPanel, -1, 'R(V)')
        self.vltsrcHbutton = wx.Button(propertyPanel, -1, 'VSrc(H)')
        self.vltsrcVbutton = wx.Button(propertyPanel, -1, 'VSrc(V)')
        self.currsrcButton = wx.Button(propertyPanel, -1, 'Iq')
        self.capacitorButton = wx.Button(propertyPanel, -1, 'C')
        
        # event routing
        self.wirebutton.Bind(wx.EVT_BUTTON, self.controller.DrawWire)
        self.resistorHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorH)
        self.resistorVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorV)
        self.vltsrcHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcH)
        self.vltsrcVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcV)
        self.currsrcButton.Bind(wx.EVT_BUTTON, self.controller.DrawCurrSrc)
        self.capacitorButton.Bind(wx.EVT_BUTTON, self.controller.DrawCapacitor)
        
        # ---------------------- / buttons --------------------------------------------- 
        
        # ----------------------- sizers -----------------------------------------------
        
        self.bhsizer = wx.BoxSizer(wx.VERTICAL)  
        self.bhsizer.Add(self.preview, 0, wx.EXPAND | wx.BOTTOM, border=0)
        self.bhsizer.Add(self.wirebutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorHbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.resistorVbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.vltsrcHbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.vltsrcVbutton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.capacitorButton, 1, wx.EXPAND | wx.BOTTOM, border=2)
        self.bhsizer.Add(self.currsrcButton, 1, wx.EXPAND | wx.BOTTOM, border=2)
            
        #self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        self.drawingBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.drawingBoxSizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=0)
        
        propertyPanel.SetSizer(self.bhsizer)
        drawingPanel.SetSizer(self.drawingBoxSizer)
        self.mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainsizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 0)
        self.mainsizer.Add(self.toolbar, 0, wx.EXPAND)
        splitter.SplitVertically(propertyPanel, drawingPanel, 150)
        self.SetSizer(self.mainsizer)
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

