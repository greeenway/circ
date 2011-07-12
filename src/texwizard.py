#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# texwizard.py - implementation of the texwizard class
# 

from element import Element

class Texwizard:
    """
    Texwizward generates the actual output of the program and/or
    prints it to a file.
    """
    def __init__(self, controller):
        self.c = controller
        self.elements = self.c.elements
        

    def GenerateCode(self):
        code = ''
        ymax = self.c.grid.y_size - 1
        
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
                    code += str(e.x)
                if e.option == 'V':
                    code += str(e.x)
                code += r'}'
                if e.option == 'H':
                    code += '{' + str(ymax - e.y) + '}'
                if e.option == 'V':
                    code += '{' + str(ymax - e.y) + '}'
                
                code += r'{' + e.option + r'}'
                code += '{}{}'
            if e.name == 'voltsrc':
                code += r'voltsrc'
                code += '{' + str(e.x) + '}{' + str(ymax - e.y) + '}'
                if e.option == 'H':
                    code += '{H}{}{}'
                else:
                    code += '{V}{}{}'
                
 
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
    
    
    
