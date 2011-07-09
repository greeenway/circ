#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# elementhandler.py - implementation of the elementhandler class
# 

import wx
import re

class Element:
    def __init__(self, name):
        self.name = name
        self.options = {}

class Elementhandler:
    def __init__(self):
        self.elements = []
        self.path = '../files/symbols/'
        self.ext = '.sym'
    
    def Readfile(self, filename):
        try:
            f = open(self.path + filename + self.ext)
            lines = [line.strip() for line in open(self.path + filename + self.ext)]
            f.close()
            
            e = Element(filename)
            cur_option = ''
            
            for line in lines:
                #print line
                if len(line) == 0 or line[0] == '#':
                    continue
                if re.search('=', line) and line[-1] == ':':
                    opt = line[:-1]
                    opt = opt.rsplit('=')
                    cur_option = opt[0]
                    e.options[cur_option] = []
                elif len(cur_option) > 0:
                    if line[0:4] == 'line' or line[0:4] == 'circ' or line[0:4] == 'rect':
                        params = line[5:-1].rsplit(',')
                        l = [line[0:4]]
                        for p in params:
                            l.append(float(p))
                        e.options[cur_option].append(l)

                    else:
                        raise Exception('Invalid format')
                        
                
                else:
                    raise Exception('Invalid format')        
        except IOError:
            print 'Cannout read ' + filename 
        except Exception:
            print 'Invalid format'
        self.elements.append(e) 
        
    def ShowElements(self):
        #debug
        for element in self.elements:
            print 'name = ' + element.name
            for option in element.options:
                print option
                for line in element.options[option]:
                    print line
    
    def GetDrawlist(self, name, option):
        for e in self.elements:
            if e.name == name:
                return e.options[option]
    


if __name__ == '__main__':
    e = Elementhandler()
    e.Readfile('resistor')
    #e.ShowElements()
    print e.GetDrawlist('resistor', 'H')
    
    
