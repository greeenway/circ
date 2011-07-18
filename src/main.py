#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# main.py - executable file of the project
# 

#TODO
# filled rects todo
# improve codegeneration code
# add text to elements.
# add red status bar on errors
# GET GUI WORKING -> custom button panel

import wx
from drawpanel import Drawpanel
from controller import Controller
from texwizard import Texwizard
from preview import Preview
from elementlist import Elementlist

from elementpattern import *

#from element import *


ID_SHOW_LOG = wx.NewId()
ID_WRITE_TEX_TO_FILE = wx.NewId()
ID_TOGGLE_BBOX = wx.NewId()
ID_REMOVE_SELECTED = wx.NewId()
ID_REMOVE_LAST = wx.NewId()
ID_ROTATE = wx.NewId()

class CButton(wx.BitmapButton):
    def __init__(self, parent, path, size=(40,40)):
         wx.BitmapButton.__init__(self, parent, -1, wx.Bitmap(path),size=size)
   
        
class SidePanel(wx.Panel):
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, size=(200,400))
        self.controller = controller
        self.buttons = []
        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.preview = Preview(self, self.controller)

        self.elements = []
        self.active = 0
        
        self.names = []
        self.options = []
        
        self.prop = wx.FlexGridSizer(4, 2, 3, 10)
        
        self.mainsizer.Add(self.preview,0 , wx.EXPAND |wx.RIGHT, 1)
        self.buttonsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainsizer.Add(self.prop, 3, wx.EXPAND |wx.ALL, 5)
        
        self.mainsizer.Add(self.buttonsizer, 5, wx.SHAPED |wx.ALL, 5)
        self.preview.OnSize()

    def SetOptions(self, pattern):
        self.ClearOptions()
        for o in pattern.options:
            if o[0] is 'LIST':
                self.AddOption(o[1], o[2:], selected = 0, text=False)
            elif o[0] is 'TEXT':
                self.AddOption(o[1], text=True, placeholder = o[2])
        self.prop.Layout()
        
    def AddButton(self, button):
        self.buttons.append(button)
        self.buttonsizer.Add(button, 1, wx.SHAPED | wx.BOTTOM, 1)
    
    def AddOption(self, name, options=[], selected = 0, text=False, placeholder = ''):
        s = wx.StaticText(self, label=name, style=wx.ALIGN_LEFT)
        if not text:
            c = wx.ComboBox(self, value=options[selected], choices=options)
        else:
            c = wx.TextCtrl(self, value = placeholder)
        self.names.append(s)
        self.options.append(c)
        self.prop.Add(s, 1, wx.EXPAND |wx.ALL) #formating not perfect : /
        self.prop.Add(c, 1, wx.EXPAND |wx.ALL)
    
    def ChangeActive(self):
        print 'change active'
        if self.controller.curPattern is not None: 
            self.SetOptions(self.controller.curPattern)
            self.controller.UpdateCanvas()
        
    
    def ClearOptions(self):
        self.prop.Clear(True)
        self.names = []
        self.options = []

        self.prop.Layout()
            
        
class PanelRLC(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        self.controller = controller
        
        #self.elements = []
        
        self.resistorPattern = Resistorpattern(self.controller.ehandler.GetPattern('resistor'))
        self.capacitorPattern = Capacitorpattern(self.controller.ehandler.GetPattern('capacitor'))
        
        
        self.resistorButton = wx.Button(self, -1, 'Resistor')  
        self.capacitorButton = wx.Button(self, -1, 'Capacitor')
        
        self.resistorButton.Bind(wx.EVT_BUTTON, self.controller.DrawResistor)
        self.capacitorButton.Bind(wx.EVT_BUTTON, self.controller.DrawCapacitor)
        
        self.AddButton(self.resistorButton)
        self.AddButton(self.capacitorButton)
        
        self.SetSizer(self.mainsizer)


class PanelSources(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        
        self.vltsrcPattern = Voltagesourcepattern(self.controller.ehandler.GetPattern('voltsrc'))
        self.cursrcPattern = Currentsourcepattern(self.controller.ehandler.GetPattern('currsrc'))
        
        #self.cur
  
        
        self.voltsrcButton = wx.Button(self, -1, 'Voltage Source')  
        self.currsrcButton = wx.Button(self, -1, 'Current Source')
        
        self.voltsrcButton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrc)
        self.currsrcButton.Bind(wx.EVT_BUTTON, self.controller.DrawCurrSrc)
        
        self.AddButton(self.voltsrcButton)
        self.AddButton(self.currsrcButton)
        
        
        
        self.SetSizer(self.mainsizer)
        
class PanelWires(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        
        self.wirePattern = Wirepattern()
        
        self.curPattern = self.wirePattern
        
        self.wireButton = wx.Button(self, -1, 'Wire')
        self.wireButton.Bind(wx.EVT_BUTTON, self.controller.DrawWire)
        self.AddButton(self.wireButton)
        
        self.SetSizer(self.mainsizer)

class PanelDiodes(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        self.test = wx.Button(self, -1, 'Diodes')
        self.AddButton(self.test)        
        self.SetSizer(self.mainsizer)

class PanelBipolar(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        self.test = wx.Button(self, -1, 'Bipolar')  
        self.AddButton(self.test)
        self.SetSizer(self.mainsizer)

class PanelOPV(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        self.test = wx.Button(self, -1, 'OPV')  
        self.AddButton(self.test)
        self.SetSizer(self.mainsizer)
        
class PanelGates(SidePanel):
    def __init__(self, parent, controller):
        SidePanel.__init__(self, parent, controller)
        self.test = wx.Button(self, -1, 'Gates')  
        self.AddButton(self.test)
        self.SetSizer(self.mainsizer)
        
class Mainwindow(wx.Frame):
    """
    Mainwindow is the main class for the GUI. 
    Beside of providing a home for Controller and Drawpanel, it
    also defines the GUI and routes Events.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900,600))

        self.controller = Controller(self) 
        self.drawpanel = Drawpanel(self, self.controller)

        nb = wx.Notebook(self, -1, style=wx.NB_RIGHT)
        nb.SetPageSize((20,400)) #..
        
        self.PanelRLC = PanelRLC(nb, self.controller)
        self.PanelSources = PanelSources(nb, self.controller)
        self.PanelWires = PanelWires(nb, self.controller)
        self.PanelDiodes = PanelDiodes(nb, self.controller)
        self.PanelBipolar = PanelBipolar(nb, self.controller)
        self.PanelOPV = PanelOPV(nb, self.controller)
        self.PanelGates = PanelGates(nb, self.controller)
        
        self.pages = [ self.PanelRLC, self.PanelSources, self.PanelWires,
        self.PanelDiodes, self.PanelBipolar, self.PanelOPV, self.PanelGates ]
        self.activePage = 0
        
        nb.AddPage(self.PanelRLC,'RLC')
        nb.AddPage(self.PanelSources,'Sources')
        nb.AddPage(self.PanelWires,'Wire & Nodes ')
        nb.AddPage(self.PanelDiodes,'Diodes')
        nb.AddPage(self.PanelBipolar,'Bipolar')
        nb.AddPage(self.PanelOPV,'OPVs')
        nb.AddPage(self.PanelGates,'Gates')

        nb.ChangeSelection(1)
        nb.ChangeSelection(self.activePage)
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNbChange)
        
        self.mainsizer = wx.BoxSizer(wx.HORIZONTAL) 
        self.mainsizer.Add(nb, 5, wx.EXPAND | wx.ALL, border=0)
        self.mainsizer.Add(self.drawpanel  , 8, wx.EXPAND | wx.ALL, border=0)
        
        
        self.SetSizer(self.mainsizer)
        self.SetAutoLayout(1)
        
        
        self.CreateStatusBar()
        
        self.toolbar = wx.ToolBar(self, -1, style=wx.TB_VERTICAL)
        self.toolbar.AddLabelTool(ID_REMOVE_LAST, 'Back', wx.Bitmap('../files/images/back.png'))
        self.toolbar.AddLabelTool(ID_REMOVE_SELECTED, 'Delete', wx.Bitmap('../files/images/delete.png'))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.controller.OnRemoveLast, id=ID_REMOVE_LAST)
        self.Bind(wx.EVT_TOOL, self.controller.DeleteSelectedElements, id=ID_REMOVE_SELECTED)
        
        self.mainsizer.Add(self.toolbar, 0, wx.EXPAND | wx.ALL, border=0)
        
        # ------------------------- create menue ------------------------------------------
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
        
        # event routing
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnClose)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.controller.OnAbout)
        wx.EVT_MENU(self, ID_WRITE_TEX_TO_FILE, self.controller.OnWriteCodeToFile) 
        wx.EVT_MENU(self, ID_REMOVE_SELECTED, self.controller.DeleteSelectedElements)
        wx.EVT_MENU(self, ID_REMOVE_LAST, self.controller.OnRemoveLast)
        wx.EVT_MENU(self, ID_ROTATE, self.controller.OnRotate)
        
        
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
        # self.buttons = []

        # self.wirebutton = wx.Button(propertyPanel, -1, 'wire')  
        # self.resistorHbutton = wx.Button(propertyPanel, -1, 'R(H)')
        # self.resistorVbutton = wx.Button(propertyPanel, -1, 'R(V)')
        # self.vltsrcHbutton = wx.Button(propertyPanel, -1, 'VSrc(H)')
        # self.vltsrcVbutton = wx.Button(propertyPanel, -1, 'VSrc(V)')
        # self.currsrcButton = wx.Button(propertyPanel, -1, 'Iq')
        # self.capacitorButton = wx.Button(propertyPanel, -1, 'C')
        
        # event routing
        # self.wirebutton.Bind(wx.EVT_BUTTON, self.controller.DrawWire)
        # self.resistorHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorH)
        # self.resistorVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawResistorV)
        # self.vltsrcHbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcH)
        # self.vltsrcVbutton.Bind(wx.EVT_BUTTON, self.controller.DrawVoltSrcV)
        # self.currsrcButton.Bind(wx.EVT_BUTTON, self.controller.DrawCurrSrc)
        # self.capacitorButton.Bind(wx.EVT_BUTTON, self.controller.DrawCapacitor)
        
        # ---------------------- / buttons --------------------------------------------- 
        
        # ----------------------- sizers -----------------------------------------------
        
        # self.bhsizer = wx.BoxSizer(wx.VERTICAL)  
        # self.bhsizer.Add(self.preview, 0, wx.EXPAND | wx.BOTTOM, border=0)
        ###

        ###
        # self.bhsizer.Add(self.wirebutton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.resistorHbutton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.resistorVbutton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.vltsrcHbutton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.vltsrcVbutton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.capacitorButton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        # self.bhsizer.Add(self.currsrcButton, 0, wx.EXPAND | wx.BOTTOM, border=2)
        
        # self.bhsizer.Add(self.searchbar, 0, wx.EXPAND | wx.BOTTOM, border=2)
        #self.bhsizer.Add(self.elementlist, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=0)
        # self.bhsizer.Add(nb, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=0)   
        
        #self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        # self.drawingBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.drawingBoxSizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=0)
        
        # propertyPanel.SetSizer(self.bhsizer)
        # drawingPanel.SetSizer(self.drawingBoxSizer)
        # self.mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.mainsizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 0)
        # self.mainsizer.Add(self.toolbar, 0, wx.EXPAND)
        # splitter.SplitVertically(propertyPanel, drawingPanel, 150)
        # self.SetSizer(self.mainsizer)
        # self.SetAutoLayout(1)
        # ----------------------- / sizers -----------------------------------------------
        self.controller.toDraw = 'resistor'
        self.controller.toDrawOption = 'H'
        self.Show(True)
    
    def OnShowLog(self, event):

        print self.controller.PrintLog()
        #self.pages[self.activePage].ClearOptions()
        #self.pages[self.activePage].AddOption('Lukas', ['A', 'B', 'C'])
        #self.pages[self.activePage].prop.Layout()
    
    def OnClose(self, event):
        self.Close()
    
    def OnNbChange(self, event):
        print 'notebook change. selection: ' + str(event.GetSelection())
        self.activePage = event.GetSelection()
        
        

if __name__ == '__main__':        
    app = wx.App(False)
    frame = Mainwindow(None, 'CIRC')
    frame.Show()
    app.MainLoop()

