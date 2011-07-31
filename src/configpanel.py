#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# configpanel.py - implementation of the ConfigPanel class
#
import wx

from preview import Preview
from propertyoption import Propertyoption

FILEPATH = '../files/images/icons/'
EXT = '.png'

class ElementTree(wx.TreeCtrl):
    def __init__(self, parent, controller):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_HIDE_ROOT)
        self.c = controller
        self.e = self.AddRoot('e')
        self.imageList = wx.ImageList(24,24)
        self.imgIdHash = {}
        self.nodeHash = {}
        
        #Passive
        #Connections&Power
        #Sources
        #Diodes
        #Transistors
        #ICs
        
        passive = self.add_node(self.e, 'passive', 'Passive')
        sources = self.add_node(self.e, 'sources', 'Sources')
        connections_power = self.add_node(self.e, 'connections', 'Connections & Power')
        diodes = self.add_node(self.e, 'diodes', 'Diodes')
        transistors = self.add_node(self.e, 'transistors', 'Transistors')
        ics = self.add_node(self.e, 'ics', 'ICs')
        
        resistor = self.add_node(passive, 'resistor', 'Resistor')
        capacitor = self.add_node(passive, 'capacitor', 'Capacitor')
        inductor = self.add_node(passive, 'inductor', 'Inductor')
        
        voltsrc = self.add_node(sources, 'voltsrc', 'VoltageSource')
        voltsrc = self.add_node(sources, 'currsrc', 'CurrentSource')
        
        wire = self.add_node(connections_power, 'wire', 'Wire')
        junct = self.add_node(connections_power, 'junct', 'Junction')
        
        self.AssignImageList(self.imageList)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelected)
        #self.Expand(passive)
        
        
    
    def add_node(self, parent, name, title=''):
        """adds node, name has to be the same as the icon name"""
        if title:
            node = self.AppendItem(parent, title)
            self.nodeHash[title] = node
        else:
            node = self.AppendItem(parent, name)

        filename = FILEPATH + name + EXT
        img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        id = self.imageList.Add(img)
        self.imgIdHash[name] = id
        
        self.SetItemImage(node, self.imgIdHash[name])
        return node
        
    
    def onSelected(self, event):
        #print self.GetItemText(event.GetItem())
        self.c.change_patterns(self.GetItemText(event.GetItem()))
        self.c.change_mode('INSERT') #move somewhere else...
        self.c.main.configpanel.propExplorer.ChangeActive()
        self.c.main.configpanel.update_properties() 

        
class PropertyExplorer(wx.Panel):
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, style=wx.BORDER_RAISED)
        self.c = controller
        self.properties = []
        
        self.prop = wx.FlexGridSizer(4, 2, 3, 10)
        self.prop.AddGrowableCol(1)
        self.SetSizer(self.prop)
    
    def AddButton(self, button):
        self.buttons.append(button)
        self.buttonsizer.Add(button, 1, wx.SHAPED | wx.BOTTOM, 5)


    def ChangeActive(self):
        """Loads properties into the sidepanel"""
        if self.c.curPattern is not None: 
            self.ClearOptions()
            if not self.c.curPattern.options:
                pass #maybe display text?
            for p in self.c.curPattern.options:
                if p[0] is 'LIST':
                    self.properties.append(
                        Propertyoption(self, self.prop, self.c,
                                       name=p[1], type='LIST', list=p[2:])
                    )
                elif p[0] is 'TEXT':
                    self.properties.append(
                        Propertyoption(self, self.prop, self.c,
                                       name=p[1], type='TEXT',
                                       defaultvalue=p[2])
                    )
            
            #sucks a bit performance wise... (but works! =)
            for key, value in self.c.curPattern.cur_options.iteritems():
                self.ChangeProperty(key,value)
            
            self.prop.Layout()
    
    def ClearOptions(self):
        self.prop.Clear(True)
        self.properties = []

    def ChangeProperty(self, name, value):
        for p in self.properties:
            if p.name == name:
                p.ChangeProperty(name,value)
    
    def GetProperty(self, name):
        for p in self.properties:
            if p.name == name:
                return p.value
        
class ConfigPanel(wx.Panel):
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, style=wx.BORDER_RAISED)
        self.c = controller
        
        self.tree = ElementTree(self, self.c)
        self.searchbar = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.preview = Preview(self, self.c)
        self.propExplorer = PropertyExplorer(self, self.c)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 3, wx.EXPAND|wx.BOTTOM, 5)#, wx.TOP)
        sizer.Add(self.searchbar, 0, wx.EXPAND|wx.BOTTOM, 5)
        sizer.Add(self.preview, 2, wx.EXPAND|wx.ALL)
        sizer.Add(self.propExplorer, 2, wx.EXPAND|wx.ALL)
        
        self.Bind(wx.EVT_TEXT, self.c.on_searchbar_change, self.searchbar)
        self.searchbar.SetFocus()
        self.SetSizer(sizer)
    
    def update_preview(self):
        self.preview.UpdateDrawing()
    
    def update_properties(self):
        self.propExplorer.ChangeActive()
    
    
    
