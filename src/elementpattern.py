#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# elementpattern.py - implementation of the Elementpattern class
# 

from element import Element
from geometry import Rectangle

import copy

class Elementpattern:
    def __init__(self, dpattern):
        if dpattern is not None:
            self.name = dpattern.name
            self.doptions = dpattern.options #hash
            self.dnames = []                 #keys
            for option in dpattern.options:
                    self.dnames.append(option)
                
        self.options = []
        self.cur_options = {}
        self.special = None
        self.name = ''
        self.sample = None
        self.olists = {}
        
    
    def CreateElement(self):
        """
        Creates an element, with the current configuration 
        """
    def UpdateSample(self):
        pass
     
    def ChangeOrientation(self, orientation):
        pass
    
    def Rotate(self):
        if self.cur_options['Orientation'] is 'V':
            self.cur_options['Orientation'] = 'H'
        else:
            self.cur_options['Orientation'] = 'V'
        
    def GetDrawlist(self, options):
        # append text directives here (to the returned object)
        if self.special is not None:
            if self.special is 'wire':
                return 'wire'
        
        return self.doptions[options['Orientation']]
    
    def ChangeOrientation(self, orientation): #make this global for all patterns
        newlist = []
        for i, list in enumerate(self.options):
            if list[1] == 'Textorientation':
                newlist = list
                break
        newlist = newlist[0:2]
        newlist.extend(self.olists[orientation])
        self.options.remove(list)
        self.options.insert(i, newlist)

class Resistorpattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.olists['H'] = ['ud', 'u', 'uu', 'c', 'd', 'dd', 
                            'l', 'uc', 'ud', 'cd', 'r', 'lc', 'cl', 'rc', 'cr', 'hu', 'hd']
        self.olists['V'] = ['l', 'r', 'lr']
        self.options.append(['LIST', 'Orientation', 'H','V'])
        l = ['LIST', 'Textorientation']
        l.extend(self.olists['H'])
        self.options.append(l)
        self.options.append(['TEXT', 'Name', 'R1'])
        self.options.append(['TEXT', 'Value', '100k'])
        
        
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Textorientation'] = 'ud'
        self.cur_options['Name'] = 'R'
        self.cur_options['Value'] = '100k'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
        self.name = 'resis'

                
    
    def UpdateSample(self):
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
        self.olists['H'] = ['hl', 'hr', 'ud', 'u', 'uu', 'c', 'd', 'dd', 
                            'l', 'uc', 'ud', 'cd', 'r', 'lc', 'cl', 'rc', 'cr', 'hu', 'hd']
        self.olists['V'] = ['r', 'l', 'u', 'd']
        self.options.append(['LIST', 'Orientation', 'H','V'])
        l = ['LIST', 'Textorientation']
        l.extend(self.olists['H'])
        self.options.append(l)
        
        self.options.append(['TEXT', 'Name', 'C1'])
        self.options.append(['TEXT', 'Value', '33n'])
        
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Textorientation'] = 'hl' #todo
        self.cur_options['Name'] = 'C'
        self.cur_options['Value'] = '33n'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
        self.name = 'capac'
    
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

class Inductorpattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.olists['H'] = ['ud', 'u', 'uu', 'd', 'dd', 
                            'l', 'ud', 'r','hu', 'hd']
        self.olists['V'] = ['l', 'r', 'lr']
        self.options.append(['LIST', 'Orientation', 'H','V'])
        l = ['LIST', 'Textorientation']
        l.extend(self.olists['H'])
        self.options.append(l)
        
        self.options.append(['TEXT', 'Name', 'L1'])
        self.options.append(['TEXT', 'Value', '100 mH'])
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Textorientation'] = 'hr' 
        self.cur_options['Name'] = 'L'
        self.cur_options['Value'] = '150 mH'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
        self.name = 'induc'
    
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
        
class Voltagesourcepattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.olists['H'] = ['ud', 'u', 'uu', 'c', 'd', 'dd', 
                            'l', 'uc', 'ud', 'cd', 'r', 'lc', 'cl', 'rc', 'cr', 'hu', 'hd']
        self.olists['V'] = ['l', 'r', 'lr']
        self.options.append(['LIST', 'Orientation', 'H','V'])
        l = ['LIST', 'Textorientation']
        l.extend(self.olists['H'])
        self.options.append(l)
        
        self.options.append(['TEXT', 'Name', 'Uq'])
        self.options.append(['TEXT', 'Value', '5 V'])
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Textorientation'] = 'ud'
        self.cur_options['Name'] = 'Uq'
        self.cur_options['Value'] = '5 V'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
        self.name = 'voltsrc'
    
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
        
class Currentsourcepattern(Elementpattern):
    def __init__(self, dpattern):
        Elementpattern.__init__(self, dpattern)
        self.olists['H'] = ['ud', 'u', 'uu', 'c', 'd', 'dd', 
                            'l', 'uc', 'ud', 'cd', 'r', 'lc', 'cl', 'rc', 'cr', 'hu', 'hd']
        self.olists['V'] = ['l', 'r', 'lr']
        self.options.append(['LIST', 'Orientation', 'H','V'])
        l = ['LIST', 'Textorientation']
        l.extend(self.olists['H'])
        self.options.append(l)
        
        self.options.append(['TEXT', 'Name', 'Iq'])
        self.options.append(['TEXT', 'Value', '2 A'])
        self.cur_options['Orientation'] = 'H'
        self.cur_options['Textorientation'] = 'ud'
        self.cur_options['Name'] = 'Iq'
        self.cur_options['Value'] = '2 A'
        self.sample = self.CreateElement(0, 0, x2 = 0, y2 = 0)
        self.name = 'currsrc'
    
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
        
class Wirepattern(Elementpattern):
    def __init__(self):
        Elementpattern.__init__(self, None)
        #self.options.append(['LIST', 'Orientation', 'H','V'])
        #self.cur_options['Value'] = '2 A'
        self.sample = self.CreateElement(0, 0, 10, 0)
        self.name = 'wire'
    
    def CreateElement(self, x, y, x2, y2):
        ne = Element(x, y, x2, y2)
        ne.pattern = self
        ne.x = x
        ne.y = y
        ne.x2 = x2
        ne.y2 = y2
        self.special = 'wire'
        ne.name = 'wire'
        d = self.GetDrawlist(self.cur_options)
        return ne
        
        
        
        
        
        
        
        
        
