#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# artist.py - implementation of the artist class
# 
import wx

HOVERED = (0, 255, 0)#(255, 250, 170)
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
    
    def DrawElement(self, dc, elem, preview = False, px = 0 , py = 0, ps = 0):
              
        dlist = elem.GetDrawlist()
        s = self.c.grid.ndist
        textPos = None
        
        x = elem.x
        y = elem.y
        x2 = elem.x2
        y2 = elem.y2
        
        if preview:
            s = ps
            x = px
            y = py
        else:
            s = self.c.grid.ndist
            x = x * s + self.c.grid.x
            y = y * s + self.c.grid.y 
            x2 = x2 * s + self.c.grid.x
            y2 = y2 * s + self.c.grid.y
            
            font1 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Arial')
            dc.SetFont(font1)

        thick = 0
        oldcolor = self.color
        
        if dlist is 'wire':
            if elem.selected or elem.hovered:
                if elem.selected:
                    dc.SetPen(wx.Pen(SELECTED, width=2))
                else:
                    dc.SetPen(wx.Pen(HOVERED, width=3))
                dc.DrawLine(x, y, x2, y2)
                dc.SetPen(wx.Pen((0,0,0), width=1))
                dc.DrawLine(x, y, x2, y2)
            else:
                dc.SetPen(wx.Pen((0,0,0), width=1))
                dc.DrawLine(x, y, x2, y2)
        
        if isinstance(dlist[0], dict):
            #print 'dict found.'
            textPos = dlist[0]
            dlist = dlist[1:]
        
        for d in dlist:    
            dc.SetBrush(wx.Brush(self.color, wx.TRANSPARENT ))
            for i in range(2):
                if elem.selected or elem.hovered:
                    if i is 0:
                        thick = 5
                        if elem.selected:
                            self.color = SELECTED
                        else:
                            self.color = HOVERED
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
                    if d[5] == 1:
                        dc.SetBrush(wx.Brush(self.color, wx.SOLID ))
                    else:
                        dc.SetBrush(wx.Brush(self.color, wx.TRANSPARENT ))
                    dc.SetPen(wx.Pen(self.color, width=d[4]+thick) )
                    dc.DrawCircle(x+d[1]*s, y +d[2]*s , d[3]*s)
                elif d[0] == 'bbox' and self.c.settings.drawboundingbox:
                    dc.SetPen(wx.Pen(HOVERED, width=1) )
                    dc.DrawRectangle(x+d[1]*s, y + d[2]*s  , d[3]*s+1, d[4]*s+1)
                elif d[0] == 'arc1':
                    dc.SetPen(wx.Pen(self.color, width=d[7]+thick))
                    dc.DrawArc(x+d[1]*s, y+d[2]*s, x+d[3]*s, y+d[4]*s, x+d[5]*s, y+d[6]*s)

        if textPos:
            if 'Textorientation' in elem.options and 'Orientation' in elem.options:
                option = elem.options['Textorientation']
                name = elem.options['Name']
                value = elem.options['Value']
                if elem.options['Orientation'] == 'H':
                    if option in ['u', 'uu', 'c', 'cc', 'd', 'dd']: #individual positioning
                        if option == 'u':
                            if name and value:
                                dc.DrawLabel(name + '  ' + value, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif name:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif value:
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                        elif option == 'uu':
                            if name and value:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['u1'][0]-1, y+s*textPos['u1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif name:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif value:
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                        elif option == 'c':
                            if name and value:
                                dc.DrawLabel(name + '  ' + value, wx.Rect(x + s*textPos['c1'][0]-1, y+s*textPos['c1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif name:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['c1'][0]-1, y+s*textPos['c1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif value:
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['c1'][0]-1, y+s*textPos['c1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                        elif option == 'cc': #transistor bullshit
                            pass
                        elif option == 'd':
                            if name and value:
                                dc.DrawLabel(name + '  ' + value, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif name:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif value:
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                        
                        elif option == 'dd':
                            if name and value:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['d2'][0]-1, y+s*textPos['d2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif name:
                                dc.DrawLabel(name, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                            elif value:
                                dc.DrawLabel(value, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                    else:
                        if option == 'l':
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        elif option == 'r':
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                        elif option == 'hu':
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                        elif option == 'hd':
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                        elif option == 'hl': 
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            
                        elif option == 'hr': 
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                         alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)

                        if option in ['uc', 'ud', 'cd', 'lc', 'cl', 'rc', 'cr']:
                            text = name
                            for i in range(2):
                                if i > 0:
                                    text = value
                                
                                if option[i] == 'u':
                                    dc.DrawLabel(text, wx.Rect(x + s*textPos['u2'][0]-1, y+s*textPos['u2'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                                elif option[i] == 'c':
                                    dc.DrawLabel(text, wx.Rect(x + s*textPos['c1'][0]-1, y+s*textPos['c1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                                elif option[i] == 'd':
                                    dc.DrawLabel(text, wx.Rect(x + s*textPos['d1'][0]-1, y+s*textPos['d1'][1]-1,2, 2), 
                                     alignment=wx.ALIGN_CENTER|wx.ALIGN_CENTER)
                                elif option[i] == 'r':
                                    if text == name:
                                        dc.DrawLabel(text, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT )
                                    else:
                                        dc.DrawLabel(text, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                                elif option[i] == 'l':
                                    if text == name:
                                        dc.DrawLabel(text, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT )
                                    else:
                                        dc.DrawLabel(text, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                if elem.options['Orientation'] == 'V':
                    if option == 'l':
                        if name and value:
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        elif name:
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['lc'][0]-1, y+s*textPos['lc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        elif value:
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['lc'][0]-1, y+s*textPos['lc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                    elif option == 'r':
                        if name and value:
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                        elif name:
                            dc.DrawLabel(name, wx.Rect(x + s*textPos['rc'][0]-1, y+s*textPos['rc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                        elif value:
                            dc.DrawLabel(value, wx.Rect(x + s*textPos['rc'][0]-1, y+s*textPos['rc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                    elif option == 'lr':
                        dc.DrawLabel(name, wx.Rect(x + s*textPos['lc'][0]-1, y+s*textPos['lc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        dc.DrawLabel(value, wx.Rect(x + s*textPos['rc'][0]-1, y+s*textPos['rc'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                    elif option == 'u':
                        dc.DrawLabel(name, wx.Rect(x + s*textPos['l1'][0]-1, y+s*textPos['l1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        dc.DrawLabel(value, wx.Rect(x + s*textPos['r1'][0]-1, y+s*textPos['r1'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                    elif option == 'd': #exists?
                        dc.DrawLabel(name, wx.Rect(x + s*textPos['l2'][0]-1, y+s*textPos['l2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
                        dc.DrawLabel(value, wx.Rect(x + s*textPos['r2'][0]-1, y+s*textPos['r2'][1]-1,2, 2), 
                                            alignment=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
                    else:
                        print option
                        print 'option not implemented'
                    
                    #todo
                    if option == 'hl':
                        pass
                    if option == 'hr':
                        pass
                    if option == 'u':
                        pass
                    if option == 'd':
                        pass
  
                    
                
                
                
                    
         
         
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
            dc.SetPen(wx.Pen(SELECTED, width=2) )
            dc.DrawCircle( x + a.x * s, y + a.y*s, 2)
    
    def DrawSelectionBox(self, dc, rect):
        dc.SetPen(wx.Pen(HOVERED, width=1) )
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT))
        s = self.c.grid.ndist
        x1 = rect[0] * s + self.c.grid.x
        y1 = rect[1] * s + self.c.grid.y 
        x2 = rect[2] * s + self.c.grid.x
        y2 = rect[3] * s + self.c.grid.y
        dc.DrawRectangle(x1, y1, (x2-x1), (y2-y1))
        #print 'drawn'
        

