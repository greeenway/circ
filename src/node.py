#!/usr/bin/env python
# circ - a gui for generating LaTeX code 
# node.py - implementation of the node class
# 

class Node:
    """
    Node represents a node in the grid.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = False