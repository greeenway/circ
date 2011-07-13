#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# artist.py - implementation of the artist class
# 
import wx

LIGHTBLUE = (0, 0, 255)
SELECTED = (255, 204, 0)

class Artist:
    """
    provides a wrapper to the drawing function
    """
    def __init__(self, controller):
        self.c = controller
        self.color = (255, 255, 255)

    def DrawWire(self, dc, x1, y1, x2, y2, s, preview = False):
        #mh...
        dc.SetPen(wx.Pen(self.color, width=1) ) #constant sucks.
        if not preview:
            x1 = x1*s + self.c.grid.x
            y1 = y1*s + self.c.grid.y
            x2 = x2*s + self.c.grid.x
            y2 = y2*s + self.c.grid.y
        dc.DrawLine(x1, y1, x2, y2)
    
    def DrawElement(self, dc, name, option, x, y, s, bbox = False, selected = False, preview = False):
              
        dlist = self.c.ehandler.GetDrawlist(name, option)
        if not preview:
            x = x * s + self.c.grid.x
            y = y * s + self.c.grid.y 
        
        #the asymmetric resistor (rect) problem:
        #it is needed to add linewidth to the rect-width
        #despite this the value 1.88 seems to leads to some rounding errors,
        #eg. 2.0 produces a totally symmetric result
        thick = 0
        oldcolor = self.color
        
        for d in dlist:
            for i in range(2):
                if selected:
                    if i is 0:
                        thick = 5
                        self.color = SELECTED
                    else:
                        thick = 0
                        self.color = oldcolor
            
                if d[0] == 'line':
                    dc.SetPen(wx.Pen(self.color, width=d[5]+thick) )
                    dc.DrawLine(x + d[1] * s, y + d[2]* s, x + d[3] *s, y + d[4]*s)
                elif d[0] == 'rect':
                    dc.SetPen(wx.Pen(self.color, width=d[5]+thick) )
                    dc.DrawRectangle(x+d[1]*s, y +d[2]*s  , d[3]*s+1*d[5], d[4]*s+1*d[5]) 
                elif d[0] == 'circ':
                    dc.SetPen(wx.Pen(self.color, width=d[4]+thick) )
                    dc.DrawCircle(x+d[1]*s, y +d[2]*s , d[3]*s)
                elif d[0] == 'bbox' and bbox:
                    dc.SetPen(wx.Pen(LIGHTBLUE, width=1) )
                    dc.DrawRectangle(x+d[1]*s, y + d[2]*s  , d[3]*s+1, d[4]*s+1)

                    
    def DrawNodes(self, dc, x, y):
        dc.SetPen(wx.Pen("grey", width=1) )
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        s = self.c.grid.ndist
        dc.SetPen(wx.Pen("black", width=1) )
        for n in  self.c.grid.nodes:
            #dc.DrawCircle( x + n.x * s, y + n.y*s, 1)
            dc.DrawPoint( x + n.x * s, y + n.y*s)
        #dc.SetPen(wx.Pen("black", width=2) )
        a = self.c.grid.an
        if a:
            dc.DrawCircle( x + a.x * s, y + a.y*s, 3)

