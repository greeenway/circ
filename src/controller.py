#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# controller.py - implementation of the controller class
# 

from texwizard import Texwizard
from elementhandler import Elementhandler
from settings import Settings
from artist import Artist
from settingsframe import Settingsframe
from grid import Grid
            
import wx

class Controller:
    """
    The Controller class is the applications's 'workhorse'.
    All Events are routed to this class and needed informations is
    stored here. Contains lots of event handlers and code to change
    what is effictivly drawn to the Drawpanel.
    """
    def __init__(self, main):
        self.elements = []
        #helper classes
        
        self.ehandler = Elementhandler()
        self.settings = Settings()
        self.t = Texwizard(self)
        self.grid = Grid(x_size=30, y_size=30, nodedistance=13, x=20, y=20)
        self.artist = Artist(self)
        self.curPattern = None
        self.mode = 'SELECT'
        self.lastSize = None
        self.selectionBox = [4, 5, 10, 12]
        
        #link
        self.main = main
        
        self.log = []
        
        #vars 
        self.leftdown = False
        
        #init
        self.ehandler.Readfile('resistor') #nach handler verschieben?!
        self.ehandler.Readfile('voltsrc')
        self.ehandler.Readfile('capacitor')
        self.ehandler.Readfile('currsrc')
        self.ehandler.Readfile('inductor')
        
        #self.toDraw = None
        #self.toDrawOption = None
        
    def PrintLog(self):
        res = ''
        for entry in self.log:
            res += entry
            res += '\n'
        return res
        
    def OnRotate(self, event=None):
        if self.curPattern:
            self.curPattern.sample.Rotate()
            self.curPattern.Rotate()
        
        for e in self.elements:
            if e.selected:
                e.Rotate()
        
        page = self.main.pages[self.main.activePage]
        cur = page.GetProperty('Orientation')
        if cur == 'V':
            page.ChangeProperty('Orientation', 'H')
            self.curPattern.ChangeOrientation('H')
        else:
            page.ChangeProperty('Orientation', 'V')
            self.curPattern.ChangeOrientation('V')
        page.ChangeActive()
        
        self.UpdateCanvas()
        
        
    
    def OnLeftClick(self, event):
        an = self.grid.an
        ln = self.grid.ln
        
        if an is None:
            return
        if self.mode == 'INSERT':
            if self.curPattern is not None:
                if self.curPattern.special is None:
                    elem = self.curPattern.CreateElement(an.x, an.y, x2 = 0, y2 = 0)
                    self.elements.append(elem)
                    
                if self.curPattern.special is 'wire':
                    if ln is None:
                        self.grid.ln = an
                return
                 
        elif self.mode == 'SELECT':
            #wires = [elem for elem in self.elements if elem.name == 'wire']
            #print len(wires)
            found = self.SelectWires(event.GetX(), event.GetY())
            if found:
                self.UpdateCanvas()
                return
            
            for e in self.elements:
                if e.bbox is not None:
                    if self.IsInBoundingBox(event.GetX(), event.GetY(), e.bbox):
                        e.selected = not e.selected
                       
                        self.UpdateCanvas()
                        return
        
        
        
        #start
        self.mode = 'SELECTBOX'
        self.selectionBox = [self.grid.an.x, self.grid.an.y, self.grid.an.x+1, self.grid.an.y+1]
        self.UpdateCanvas()

    
    
    def SelectWires(self, x, y, mode='pick'):
        """select wires, todo rewrite in pretty form"""
        wires = [elem for elem in self.elements if elem.name == 'wire']
        s = self.grid.ndist
        xp = self.grid.x
        yp = self.grid.y

        
        selection = []
        
        for wire in wires:
            x1 = wire.x * s + xp
            x2 = wire.x2 * s + xp
            y1 = wire.y * s + yp
            y2 = wire.y2 * s + yp
            div = (x2-x1)**2+(y2-y1)**2*1.0
            t = ((x2-x1)*(x-x1)+(y2-y1)*(y-y1))/div
            if t < 0:
                t = 0
            elif t > 1:
                t = 1
            d = (x1+t*(x2-x1)-x)**2 + (y1+t*(y2-y1)-y)**2
            
            selection.append([wire, d])
        
        if selection:
            min = selection[0][1]
            a = 0
            
            for i in range(0,len(selection)):
                if selection[i][1] < min:
                    min = selection[i][1]
                    a = i
                    
            if min < 49: #7pixel
                if mode == 'pick':
                    selection[a][0].selected = not selection[a][0].selected
                else:
                    if not selection[a][0].selected:
                        selection[a][0].hovered = True
                
                return True
    
        return False
        
    
    def OnLeftUp(self, event):
        an = self.grid.an
        ln = self.grid.ln
        
        if an is None:
            return
        
        
        if self.mode == 'SELECTBOX':
            x1 = self.selectionBox[0]
            y1 = self.selectionBox[1]
            x2 = self.selectionBox[2]
            y2 = self.selectionBox[3]
            
            for e in self.elements:
                if e.name is not 'wire':
                    if e.bbox.x > x1 and e.bbox.y > y1 \
                            and e.bbox.x + e.bbox.w < x2 and e.bbox.y + e.bbox.h < y2:
                        e.selected = True 
                if e.name is 'wire':
                    if e.x > x1 and e.y > y1 and e.x2 < x2 and e.y2 < y2:
                        e.selected = True 
            
            
            self.mode = 'SELECT'
            self.selectionBox = None
            self.UpdateCanvas()
            return
            
        if self.curPattern is not None:
            if self.curPattern.special is 'wire':
                if ln is not None:
                    if ln is an:
                        #print 'same nodes...'
                        ln = None
                        #todo: stop creation if user is too stupid
                        return
                    elem = self.curPattern.CreateElement(ln.x, ln.y, an.x, an.y)
                    #elem.selected = True
                    self.elements.append(elem)
                    self.grid.ln = None
                    self.UpdateCanvas()
                
                
        
    def OnRightClick(self, event):
        if self.mode == 'SELECTBOX':
            self.mode = 'SELECT'
        for e in self.elements:
            if e.bbox is not None:
                if self.IsInBoundingBox(event.GetX(), event.GetY(), e.bbox):
                    
                    e.selected = not e.selected
                    self.UpdateCanvas()
         
        

    def IsInBoundingBox(self, x, y, bbox):
        b = bbox
        x = x - self.grid.x
        y = y - self.grid.y
        s = self.grid.ndist
        if b.x * s < x and (b.x + b.w )* s > x and y > b.y * s and y < (b.y+b.h) * s:
            return True
        return False
    

        
    def OnMouseOver(self, event):
        if self.grid.findActiveNode(event.GetX(), event.GetY()):
            self.UpdateCanvas()
        for e in self.elements:
            e.hovered = False
        if self.mode == 'SELECT':
            found = self.SelectWires(event.GetX(), event.GetY(), 'hover')
            if found:
                self.UpdateCanvas()
                return
            
            for e in self.elements:
                if e.bbox is not None:
                    if self.IsInBoundingBox(event.GetX(), event.GetY(), e.bbox):
                        if not e.selected:
                            e.hovered = True
                            self.UpdateCanvas()
                            return
                            
        if self.mode == 'SELECTBOX':
            if self.grid.an:
                self.selectionBox[2] = self.grid.an.x
                self.selectionBox[3] = self.grid.an.y
                x1 = self.selectionBox[0]
                y1 = self.selectionBox[1]
                x2 = self.selectionBox[2]
                y2 = self.selectionBox[3]
                
                for e in self.elements:
                    if e.name is not 'wire':
                        if e.bbox.x > x1 and e.bbox.y > y1 \
                                and e.bbox.x + e.bbox.w < x2 and e.bbox.y + e.bbox.h < y2:
                            e.hovered = True 
                    if e.name is 'wire':
                        if e.x > x1 and e.y > y1 and e.x2 < x2 and e.y2 < y2:
                            e.hovered = True 
                self.UpdateCanvas()
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self.main, 'CIRC \n a GUI frontend for circdia.sty\t\n' '2011-\t', 'About',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
                   
    def OnKeyDown(self, event):
        print 'keydown'
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE:
            print 'deletekey'
            self.DeleteSelectedElements()
    
    def OnScrollEvent(self, event=None):
        #event.GetWheelRotation() == 120 up, -120 => down
        if event.GetWheelRotation() > 0:
            self.grid.ndist += 1
        else:
            self.grid.ndist -= 1
        self.UpdateSize()
        self.UpdateCanvas()
        
    
    def OnSelect(self, event=None):
        self.mode = 'SELECT'
        
    def OnWriteCodeToFile(self, event):
        print self.t.GenerateCode()
        self.t.PrintToFile('test.tex')

    def OnToggleBoundingBox(self, event):
        self.settings.drawboundingbox = not self.settings.drawboundingbox 
        self.UpdateCanvas()
    
    def DeleteSelectedElements(self, event=None):
        new = []
        for e in self.elements:
            if not e.selected:
                new.append(e)
        self.elements = new
        self.UpdateCanvas()
    
    def OnRemoveLast(self, event=None):
        if len(self.elements) > 0:
            self.elements.pop()
        self.UpdateCanvas()
    
    def UpdateSize(self, event = None):   
        if event:
            size = event.GetSize()
            self.lastSize = size
        elif self.lastSize:
            size = self.lastSize
        else:
            return
            
        w = size[0]
        h = size[1]
        w_b = w - self.grid.ndist * self.grid.x_size
        w_h = h - self.grid.ndist * self.grid.y_size
        if w_b/2 > 0:
            self.grid.x = w_b/2
        if w_h/2 > 0:
            self.grid.y = w_h/2
    
    def DrawWire(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].wirePattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    def DrawResistor(self, event= None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].resistorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
    
    def DrawInductor(self, event=None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].inductorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    def DrawVoltSrc(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].vltsrcPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
        
    
    def DrawCapacitor(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].capacitorPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!
    
    def DrawCurrSrc(self, event = None):
        self.mode = 'INSERT'
        self.curPattern = self.main.pages[self.main.activePage].cursrcPattern
        self.main.pages[self.main.activePage].ChangeActive()
        self.UpdateCanvas() #improve!

    def SetOption(self, name, value):
        if self.curPattern is not None:
            self.curPattern.cur_options[name] = value
            self.curPattern.sample = self.curPattern.CreateElement(0, 0, x2 = 0, y2 = 0)
    
    def UpdateCanvas(self):
        
        self.main.drawpanel.UpdateDrawing()
        
        #maybe optimize this:
        self.main.pages[self.main.activePage].preview.UpdateDrawing()
        
    def OnSettings(self, event=None):
        s = Settingsframe(self.main, self)
        
        
        
        
        
        




