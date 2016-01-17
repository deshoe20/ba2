'''
Created on 14.01.2016

@author: Albert
'''
from MyNLTKTree import MyNLTKTree

class CanonicalLexiconTree(MyNLTKTree):
    '''
    classdocs
    '''


    def __init__(self, node, children=None):
        '''
        Constructor
        '''
        super().__init__(node, children)