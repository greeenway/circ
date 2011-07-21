#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# element.py - implementation of the element class
# 

class Element:
    """
    Represents a circuit element used by controller to 
    keep track of all items.
    """
    def __init__(self, x, y, x2 = 0, y2 = 0):
        self.pattern = None
        self.selected = False
        self.hovered = False
        self.showBbox = False
        self.bbox = None
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.options = {}
        self.name = ''
        
    def GetDrawlist(self):
        return self.pattern.GetDrawlist( self.options)
    
    def Rotate(self):
        if self.options['Orientation'] is 'V':
            self.options['Orientation'] = 'H'
        else:
            self.options['Orientation'] = 'V'

