#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# elementhandler.py - implementation of the elementhandler class
# 

import wx
import re

class Drawingpattern:
    def __init__(self, name):
        self.name = name
        self.options = {}      

class Elementhandler:
    """
    Elementhandler loads .sym files into memory. Provides
    information needed for drawing objects
    """
    def __init__(self):
        self.patterns = []
        self.path = '../files/symbols/'
        self.ext = '.sym'
    
    def Readfile(self, filename):
        try:
            f = open(self.path + filename + self.ext)
            lines = [line.strip() for line in open(self.path + filename + self.ext)]
            f.close()
            
            d = Drawingpattern(filename)
            cur_option = ''
            
            for line in lines:
                #print line
                if len(line) == 0 or line[0] == '#':
                    continue
                if re.search('=', line) and line[-1] == ':':
                    opt = line[:-1]
                    opt = opt.rsplit('=')
                    cur_option = opt[0]
                    d.options[cur_option] = []
                elif len(cur_option) > 0:
                    if line[0:4] == 'line' or line[0:4] == 'circ' or line[0:4] == 'rect' or line[0:4] == 'bbox':
                        params = line[5:-1].rsplit(',')
                        l = [line[0:4]]
                        for p in params:
                            l.append(float(p))
                        d.options[cur_option].append(l)

                    else:
                        raise Exception('Invalid format')
                        
                
                else:
                    raise Exception('Invalid format')        
        except IOError:
            print 'Cannout read ' + filename 
        except Exception:
            print 'Invalid format'
        self.patterns.append(d) 
        
    def ShowDrawingpatterns(self):
        #debug
        for d in self.patterns:
            print 'name = ' + d.name
            for option in d.options:
                print option
                for line in d.options[option]:
                    print line
    
    def GetDrawlist(self, name, option):
        for p in self.patterns:
            if p.name == name:
                return p.options[option]
    
    def GetPattern(self, name):
        for p in self.patterns:
            if p.name == name:
                return p
    


if __name__ == '__main__':
    e = Elementhandler()
    e.Readfile('voltsrc')
    e.ShowDrawingpatterns()
    #print e.GetDrawlist('voltsrc', 'H')
    
    
