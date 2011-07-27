#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main2.py - new executable file of the project
# 

import wx

from controller import Controller
from drawpanel import Drawpanel
from circtoolbar import CircToolbar
from configpanel import ConfigPanel

#create IDs
ID_SHOW_LOG = wx.NewId()
ID_WRITE_TEX_TO_FILE = wx.NewId()
ID_TOGGLE_BBOX = wx.NewId()
ID_REMOVE_SELECTED = wx.NewId()
ID_REMOVE_LAST = wx.NewId()
ID_ROTATE = wx.NewId()
ID_SELECT = wx.NewId()
ID_SETTINGS = wx.NewId()

class Main(wx.Frame):
    """
    Main is the main class for the GUI. 
    """
    def __init__(self):
        wx.Frame.__init__(self, None, title='CIRC', size=(900,600))
        
        
        self.controller = Controller(self) 
        self.configpanel = ConfigPanel(self, self.controller)
        self.drawpanel = Drawpanel(self, self.controller)
        self.toolbar = CircToolbar(self, self.controller)
        
        self.create_menu()
        self.bind_menu_events()
        self.CreateStatusBar()
        
        #self.SetBackgroundColour
        
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        mainsizer.Add(self.configpanel, 1, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(self.drawpanel, 3, wx.EXPAND|wx.ALL, 5)
        mainsizer.Add(self.toolbar, 0, wx.EXPAND|wx.ALL)
        
        self.SetSizer(mainsizer)
        self.SetAutoLayout(1)
    
    def create_menu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', 'Some Information.')
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program\tCtrl+Q')
        
        
        buildmenu = wx.Menu()
        buildmenu.Append(ID_WRITE_TEX_TO_FILE, '&Write Code\tCtrl+W', 'Generate LaTeX-Output (fileoutput).')
        
        editmenu = wx.Menu()
        editmenu.Append(ID_REMOVE_SELECTED, 'Remove &selected Elements', 'Remove all selected elements.')
        editmenu.Append(ID_REMOVE_LAST, 'Remove &last Element\tCtrl+Z', 'Remove the last created object.')
        editmenu.Append(ID_ROTATE, 'Rotate selected Elements\tCtrl+R', 'Rotate all selected elements.')
        editmenu.Append(ID_SETTINGS, '&Settings', 'Change Settings')
        
        #DEBUG
        debugmenu = wx.Menu()
        debugmenu.Append(ID_SHOW_LOG, 'Show &Log', 'Show Controller\'s Log')
        debugmenu.Append(ID_TOGGLE_BBOX, '&Show BoundingBoxes', kind=wx.ITEM_CHECK)
        debugmenu.Check(ID_TOGGLE_BBOX, False)

        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        menubar.Append(editmenu, '&Edit')
        menubar.Append(buildmenu, '&Build')
        menubar.Append(debugmenu, '&Debug')
        self.SetMenuBar(menubar)
    
    def bind_menu_events(self):
        wx.EVT_MENU(self, wx.ID_EXIT, self.on_close)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.on_about)
        wx.EVT_MENU(self, ID_WRITE_TEX_TO_FILE, self.controller.OnWriteCodeToFile) 
        wx.EVT_MENU(self, ID_REMOVE_SELECTED, self.controller.DeleteSelectedElements)
        wx.EVT_MENU(self, ID_REMOVE_LAST, self.controller.OnRemoveLast)
        wx.EVT_MENU(self, ID_ROTATE, self.controller.OnRotate)
        wx.EVT_MENU(self, ID_SETTINGS, self.controller.OnSettings)
    
    def on_close(self, event):
        self.Close()
    
    def on_about(self, event):
        dlg = wx.MessageDialog(self, 'CIRC \n a GUI frontend for circdia.sty\t\n' '2011-\t', 'About',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
        

if __name__ == '__main__':        
    app = wx.App(False)
    frame = Main()
    frame.Show()
    app.MainLoop()
