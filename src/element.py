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
        self.showBbox = False
        self.bbox = None
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.options = {}
        
    def GetDrawlist(self):
        return self.pattern.GetDrawlist( self.options)


        
class Resistor(Element):
    def __init__(self):
        Element.__init__(self, '', '', 0, 0, x2 = 0, y2 = 0, bbox = None)

        self.options.append(['LIST', 'Orientation', 'H','V'])
        self.options.append(['TEXT', 'Name', 'R1'])
        self.options.append(['TEXT', 'Value', '100Ohm'])
        
