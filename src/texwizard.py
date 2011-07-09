#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# texwizard.py - implementation of the texwizard class
# 

class Element:
    def __init__(self, name, option, x, y, x2 = 0, y2 = 0):
        self.name = name
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.option = option

class Texwizard:
    def __init__(self):
        self.elements = []
        self.preamble = r'\begin{circuitdiagram}{50}{50}' + '\n'
        self.ending = r'\end{circuitdiagram}' + '\n'

    def GenerateCode(self):
        code = self.preamble
        
        for e in self.elements:
            code += "\\"
            code += e.name 
           
            if len(e.option) >= 1:
                #code += r'{' + e.option + r'}'
                pass
            code += '\n'
            
            
        code += self.ending
        return code
        
    def PrintToFile(self, filename):
        f = open(filename, 'w')
        code = self.GenerateCode()
        f.write(code)
        f.close()
        
        
if __name__ == '__main__':
    t = Texwizard()
    print t.GenerateCode()
    #t.PrintToFile('test.txt')
    
    
    
