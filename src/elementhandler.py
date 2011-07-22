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
        wire = Drawingpattern('wire')
        wire.options['wire'] = True
    
    def Readfile(self, filename):
        try:
            f = open(self.path + filename + self.ext)
            lines = [line.strip() for line in open(self.path + filename + self.ext)]
            f.close()
            
            d = Drawingpattern(filename)
            cur_option = ''
            dscDict = {}
            #isinstance({}, dict) dict query
            
            for line in lines:
                #print line
                if len(line) == 0 or line[0] == '#':
                    continue
                
                    
                if re.search('=', line) and line[-1] == ':':
                    opt = line[:-1]
                    opt = opt.rsplit('=')
                    cur_option = opt[0]
                    d.options[cur_option] = []
                    dscDict = {}
                elif len(cur_option) > 0:
                    if line[0] == '@':
                        #print line[1:3]
                        #print line[4:-1].rsplit(',')
                        z = line[4:-1].rsplit(',')
                        v = [float(z[0]), -float(z[1])]
                        dscDict[line[1:3]] = v
                        continue
                
                    if line[0:4] == 'line' or line[0:4] == 'circ' or line[0:4] == 'rect' or line[0:4] == 'bbox' or \
                            line[0:4] == 'tex1' or line[0:4] == 'tex2' or line[0:4] == 'arc1':
                        if not d.options[cur_option] and dscDict:
                            d.options[cur_option].append(dscDict)
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
    e.Readfile('resistor')
    e.ShowDrawingpatterns()
    #print e.GetDrawlist('voltsrc', 'H')
    
    
