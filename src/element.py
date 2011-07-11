#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# element.py - implementation of the element class
# 

class Element:
    def __init__(self, name, option, x, y, x2 = 0, y2 = 0):
        self.name = name
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.option = option