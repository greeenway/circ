#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# texwizard.py - implementation of the texwizard class
# 

class Element:
    def __init__(self, name, option, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.option = option

class Texwizard:
    def __init__(self):
        self.elements = []
        self.preamble = r'\begin{circuitdiagram}{50}{50}'
        self.ending = r'\end{circuitdiagram}'

    def GenerateCode(self):
        code = self.preamble
        
        for element in self.elements:
            pass
            
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
