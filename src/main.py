#!/usr/bin/env python
# a hello world example from wikipedia.org

import wx

class DrawPanel(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_MOTION(self, self.onMouseOver)
    
    def OnPaint(self, event=None):
        #draw buffer to the screen
        dc = wx.BufferedPaintDC(self, self._Buffer)

    def OnSize(self, event=None):
        size  = self.ClientSize
        self._Buffer = wx.EmptyBitmap(*size)
        self.UpdateDrawing()
     
    def UpdateDrawing(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        del dc # 
        self.Refresh()
        self.Update()
        
    def onMouseOver(self, event):
        #(x-x_m)^2+(y-y_m)^2 < r^2
        print '(' + str(event.GetX()) + '/' + str(event.GetX()) + ')'
        
    def Draw(self, dc):
        dc.Clear()
        dc.SetBrush(wx.Brush("white"))
        #dc.DrawRectangle(10,10,100,100)
        
        dc.SetPen(wx.Pen("black", width=1) )
    
        red = wx.Colour(255,0,0)
        brush = wx.Brush(red, wx.TRANSPARENT)
        self.DrawGrid(dc, 300, 300)
        dc.SetBrush(brush)
        
        #dc.DrawLine(0, 10, 50, 50)
        
        #dc.DrawRectangle(10,10,50,50)
    
    def DrawGrid(self, dc, width, height, delta=15):
        x = delta
        y = delta
        while x < width:
            while y < height:
                dc.DrawCircle(x, y, 2)
                y = y + delta
            y = delta
            x = x + delta
                

        
        

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600,400))
        self.CreateStatusBar()
        
        filemenu = wx.Menu()
        
        filemenu.Append(wx.ID_ABOUT, "&About", "Some Information.")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        self.drawpanel = DrawPanel(self)
        self.buttons = []
        
        self.vsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bhsizer = wx.BoxSizer(wx.VERTICAL)
        
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "button " + str(i)))
            self.bhsizer.Add(self.buttons[i], 1, wx.EXPAND | wx.BOTTOM, border=2)
            
        self.vsizer.Add(self.bhsizer, 0, wx.EXPAND )
        self.vsizer.Add(self.drawpanel, 1, wx.EXPAND | wx.ALL, border=3)

        
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        #self.vsizer.Fit(self)
        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)
        self.Show(True)
        
        
 
app = wx.App(False)
frame = MainWindow(None, "CIRC")
frame.Show()
app.MainLoop()

