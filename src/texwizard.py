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

    def GenerateCode(self):
        lines = []
        curline = ''
        ym = self.c.grid.y_size - 1 
        
        for e in self.c.elements:
            name = e.pattern.name
            x = e.x
            y = e.y
            x2 = e.x2
            y2 = e.y2
            opt = e.options
            c = lambda t: '{' + str(t) +'}'
            
            curline = '\\'
            curline += name
            
            if name == 'wire':
                curline += c(x) + c(ym-y) + c(x2) + c(ym-y2)
            elif name in ['resis', 'capac', 'induc', 'voltsrc', 'currsrc']:
                curline += c(x) + c(ym-y)
                curline += c(opt['Orientation'] + opt['Textorientation'])
                curline += c(opt['Name'])
                curline += c(opt['Value'])

            lines.append(curline)
    
        code = ''
        for line in lines:
            code += line
            code += '%\n'
        return code
        
    def PrintToFile(self, filename):
        f = open(filename, 'w')
        
        code = r'\documentclass{article}' + '%\n'
        code += r'\usepackage{circdia}' + '%\n'
        code += r'\begin{document}' + '%\n'
        code += r'\begin{circuitdiagram}[draft]{'
        code += str(self.c.grid.x_size) + '}{'
        code += str(self.c.grid.y_size) + '}%\n'
        code += self.GenerateCode()
        code += r'\end{circuitdiagram}' + '%\n'
        code += r'\end{document}' + '%\n'
        f.write(code)
        f.close()
        
        
if __name__ == '__main__':
    t = Texwizard()
    print t.GenerateCode()
    #t.PrintToFile('test.txt')
    
    
    
