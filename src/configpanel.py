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
        
        passive = self.add_node(self.e, 'passive', 'Passive')
        sources = self.add_node(self.e, 'sources', 'Sources')
        connections = self.add_node(self.e, 'connections', 'Connections')
        
        resistor = self.add_node(passive, 'resistor', 'Resistor')
        capacitor = self.add_node(passive, 'capacitor', 'Capacitor')
        
        voltsrc = self.add_node(sources, 'voltsrc', 'VoltageSource')
        voltsrc = self.add_node(sources, 'currsrc', 'CurrentSource')
        
        wire = self.add_node(connections, 'wire', 'Wire')
        
        self.AssignImageList(self.imageList)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelected)
        
        
    
    def add_node(self, parent, name, title=''):
        """adds node, name has to be the same as the icon name"""
        if title:
            node = self.AppendItem(parent, title)
        else:
            node = self.AppendItem(parent, name)

        filename = FILEPATH + name + EXT
        img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        id = self.imageList.Add(img)
        self.imgIdHash[name] = id
        
        self.SetItemImage(node, self.imgIdHash[name])
        return node
        
    
    def onSelected(self, event):
        print self.GetItemText(event.GetItem())
        self.c.change_patterns(self.GetItemText(event.GetItem()))
        self.c.mode = 'INSERT'
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
        self.preview = Preview(self, self.c)
        self.propExplorer = PropertyExplorer(self, self.c)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND|wx.ALL)
        sizer.Add(self.preview, 1, wx.EXPAND|wx.ALL)
        sizer.Add(self.propExplorer, 1, wx.EXPAND|wx.ALL)
        
        self.SetSizer(sizer)
    
    def update_preview(self):
        self.preview.UpdateDrawing()
    
    def update_properties(self):
        self.propExplorer.ChangeActive()
    
    
    