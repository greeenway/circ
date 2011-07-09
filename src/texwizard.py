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
        self.c = None
        #self.preamble = r'\begin{circuitdiagram}{50}{50}' + '\n'
        #self.ending = r'\end{circuitdiagram}' + '\n'
    
    def init(self, controller):
        self.c = controller

    def GenerateCode(self):
        code = ''
        ymax = self.c.ynodes - 1
        
        for e in self.elements:
            code += "\\" 
            
            if e.name == 'wire':
                code += 'wire'
                code += '{' + str(e.x) + '}{' + str(ymax - e.y) + '}{'
                code += str(e.x2) + '}{' + str(ymax - e.y2) + '}'
 
            if e.name == 'resistor':
                code += 'resis'
                code += r'{'
                if e.option == 'H':
                    code += str(e.x + 3)
                if e.option == 'V':
                    code += str(e.x)
                code += r'}'
                if e.option == 'H':
                    code += '{' + str(ymax - e.y) + '}'
                if e.option == 'V':
                    code += '{' + str(ymax - e.y - 3) + '}'
                
                code += r'{' + e.option + r'}'
                code += '{}{}'
 
            code += '\n'
            
            
        #code += self.ending
        return code
        
    def PrintToFile(self, filename):
        f = open(filename, 'w')
        
        code = r'\documentclass{article}' + '\n'
        code += r'\usepackage{circdia}' + '\n'
        code += r'\begin{document}' + '\n'
        code += r'\begin{circuitdiagram}[draft]{20}{20}' + '\n'
        code += self.GenerateCode()
        code += r'\end{circuitdiagram}' + '\n'
        code += r'\end{document}' + '\n'
        f.write(code)
        f.close()
        
        
if __name__ == '__main__':
    t = Texwizard()
    print t.GenerateCode()
    #t.PrintToFile('test.txt')
    
    
    
