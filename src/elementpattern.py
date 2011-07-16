#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# elementpattern.py - implementation of the Elementpattern class
# 

from element import Element
from geometry import Rectangle

import copy

class Elementpattern:
    def __init__(self, dpattern):
        self.name = dpattern.name
        self.doptions = dpattern.options #hash
        self.dnames = []                 #keys
        for option in dpattern.options:
                self.dnames.append(option)
                
        self.options = []
        self.cur_options = {}
        
    
    def CreateElement(self):
        """
        Creates an element, with the current configuration 
        """
        
    def GetDrawlist(self, options):
        # append text directives here (to the returned object)
        return self.doptions[options['Orientation']]

class Resistorpattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.options.append(['LIST', 'Orientation', 'H','V'])
        self.options.append(['TEXT', 'Name', 'R1'])
        self.options.append(['TEXT', 'Value', '100 Ohm'])
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Name'] = 'R'
        self.cur_options['Value'] = '100 Ohm'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
    
    def CreateElement(self, x, y, x2 = 0, y2 = 0):
        ne = Element(x, y, x2, y2)
        ne.pattern = self
        ne.x = x
        ne.y = y
        ne.x2 = x2
        ne.y2 = y2
        d = self.GetDrawlist(self.cur_options)
        if d[-1][0] == 'bbox':
            ne.bbox = Rectangle(x+d[-1][1], y+ d[-1][2], d[-1][3], d[-1][4])
        ne.options = copy.deepcopy(self.cur_options)
        return ne
        
class Capacitorpattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.options.append(['LIST', 'Orientation', 'H','V'])
        self.options.append(['LIST', 'Textorientierung', 'l', 'u', 'hd', 'dd'])
        self.options.append(['TEXT', 'Name', 'R1'])
        self.options.append(['TEXT', 'Value', '100 Ohm'])
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Name'] = 'C'
        self.cur_options['Value'] = '150 muF'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
    
    def CreateElement(self, x, y, x2 = 0, y2 = 0):
        ne = Element(x, y, x2, y2)
        ne.pattern = self
        ne.x = x
        ne.y = y
        ne.x2 = x2
        ne.y2 = y2
        d = self.GetDrawlist(self.cur_options)
        if d[-1][0] == 'bbox':
            ne.bbox = Rectangle(x+d[-1][1], y+ d[-1][2], d[-1][3], d[-1][4])
        ne.options = copy.deepcopy(self.cur_options)
        return ne
        
        
        
        
        
        
        
        
        
        