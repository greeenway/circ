#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# drawpanel.py - implementation of the drawpanel class
# 

import wx
import math

from controller import Controller
from node import Node

GREY = (205, 205, 205)
BLACK = (0, 0, 0)
LIGHTBLUE = (0, 0, 255)
SELECTED = (255, 204, 0)

class Drawpanel(wx.Window):
    """
    Drawpanel is a custom drawing widget which serves as a canvas.
    Events are routed to the Controller class, where they are interpreted.
    Drawpanel receives from the controller (elementhandler)
    """
    def __init__(self, parent, controller):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetDoubleBuffered(True)
        
        self.c = controller
        self.color = (0,0,255)
        
        #events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        
        #make events local?
        wx.EVT_MOTION(self, self.c.OnMouseOver)
        wx.EVT_LEFT_DOWN(self, self.c.OnLeftClick)
        wx.EVT_RIGHT_DOWN(self, self.c.OnRightClick)
        self.Bind(wx.EVT_LEFT_UP, self.c.OnLeftUp)
        #wx.EVT_KEY_DOWN(self, self.c.OnKeyDown)
        self.Bind(wx.EVT_MOUSEWHEEL, self.c.OnScrollEvent)
    
    def OnPaint(self, event=None):
        #draw buffer to the screen
        dc = wx.BufferedPaintDC(self, self._Buffer)


    def OnSize(self, event=None):
        size  = self.ClientSize
        self._Buffer = wx.EmptyBitmap(*size)
        self.UpdateDrawing()
        self.c.UpdateSize(event)
    
     
    def UpdateDrawing(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        del dc # 
        self.Refresh()
        self.Update()
        
    def Draw(self, dc):
        #actual drawing code
        dc.Clear()
        dc.SetBrush(wx.Brush("white")) 
        dc.SetPen(wx.Pen("black", width=1) )
    
        self.c.artist.DrawNodes(dc, self.c.grid.x, self.c.grid.y)
        s = self.c.grid.ndist
        x = self.c.grid.x
        y = self.c.grid.y
        
        for e in self.c.elements:
            self.c.artist.color = BLACK
            self.c.artist.DrawElement(dc, e)
        
        ####
        # w, h = dc.GetSize()

        # wires = [elem for elem in self.c.elements if elem.name == 'wire']
        
        # if wires:
            # s = self.c.grid.ndist
            # xp = self.c.grid.x
            # yp = self.c.grid.y
            # wire = wires[0]
            # x1 = wire.x * s + xp
            # x2 = wire.x2 * s + xp
            # y1 = wire.y * s + yp
            # y2 = wire.y2 * s + yp
            
            # map = []
            
            # for x in range(w):
                # map.append([])
                # for y in range(h):
                    # map[x].append(1)
            
            # max = 0
            # for x in range(w):
                    # for y in range(h):
                        # div = (x2-x1)**2+(y2-y1)**2*1.0
                        # t = ((x2-x1)*(x-x1)+(y2-y1)*(y-y1))/div

                        # if t < 0:
                           # t = 0
                        # elif t > 1:
                           # t = 1
                        ##print t
                        # d = math.sqrt((x1+t*(x2-x1)-x)**2 + (y1+t*(y2-y1)-y)**2)
                        # map[x][y] = d
                        # if x == 25 and y == 78:
                            # print 'x = ' + str(x)
                            # print 'y = '+ str(y)
                            # print 'x1 = '+ str(x1)
                            # print 'x2 = '+ str(x2)
                            # print 'y1 = '+ str(y1)
                            # print 'y2 = '+ str(y2)
                            # print 'd = ' + str(d)
                            
                        # if d > max:
                            # max = d
            # print 'computed'   
            # print 'max = ' + str(d)
             
            # for x in range(w):
                # for y in range(h):
                    # c = 255 - (map[x][y] / (max*1.0) * 254)
                    # dc.SetPen(wx.Pen((c,c,c), width=1) )
                    # dc.DrawPoint(x,y) 
            
            # self.c.artist.color = SELECTED
            # self.c.artist.DrawElement(dc, wire)
        
        ###
    
        #draw active
        
        if self.c.mode == 'SELECTBOX':
            if self.c.selectionBox:
                self.c.artist.DrawSelectionBox(dc, self.c.selectionBox)
        
        if self.c.mode == 'INSERT':
            self.c.artist.color = GREY
            if self.c.curPattern is not None and self.c.grid.an is not None:
                if self.c.curPattern.special is 'wire':
                    if self.c.grid.ln is not None and self.c.grid.an is not None:
                        self.c.curPattern.sample.x = self.c.grid.ln.x
                        self.c.curPattern.sample.y = self.c.grid.ln.y
                        self.c.curPattern.sample.x2 = self.c.grid.an.x
                        self.c.curPattern.sample.y2 = self.c.grid.an.y
                        self.c.artist.DrawElement(dc, self.c.curPattern.sample)
                        
                else:
                    self.c.curPattern.sample.x = self.c.grid.an.x #wire to do
                    self.c.curPattern.sample.y = self.c.grid.an.y
                    self.c.artist.DrawElement(dc, self.c.curPattern.sample)
            
    
    
    
    
    
