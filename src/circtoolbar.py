#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# circtoolbar.py - implementation of the CircToolbar class
#

import wx

ID_RM_LAST = wx.NewId()
ID_DEL_SEL_ELEMENTS = wx.NewId()
ID_ON_SELECT = wx.NewId()

class CircToolbar(wx.ToolBar):
    def __init__(self, parent, controller):
        wx.ToolBar.__init__(self, parent, id=wx.ID_ANY, style=wx.TB_VERTICAL)
        self.c = controller
        
        get_bmp = wx.ArtProvider.GetBitmap
        size = (32,32)
        self.AddLabelTool(ID_RM_LAST, 'Select', get_bmp(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, size))
        self.AddLabelTool(ID_DEL_SEL_ELEMENTS, 'Delete',get_bmp(wx.ART_DELETE, wx.ART_TOOLBAR, size))
        self.AddLabelTool(ID_ON_SELECT, 'Back', get_bmp(wx.ART_UNDO, wx.ART_TOOLBAR, size))
        
        self.bind_events()
        
        self.Realize()
    
    def bind_events(self):
        #self.Bind(wx.EVT_TOOL, self.c.OnRemoveLast, id=ID_RM_LAST) #get this working...
        #self.Bind(wx.EVT_TOOL, self.c.DeleteSelectedElements, id=ID_DEL_SEL_ELEMENTS)
        #self.Bind(wx.EVT_TOOL, self.c.OnSelect, id=ID_ON_SELECT)
        wx.EVT_TOOL(self, ID_RM_LAST, self.c.OnRemoveLast)
        wx.EVT_TOOL(self, ID_DEL_SEL_ELEMENTS, self.c.DeleteSelectedElements)
        wx.EVT_TOOL(self, ID_ON_SELECT, self.c.OnSelect)