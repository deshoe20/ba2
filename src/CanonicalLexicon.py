'''
Created on 04.01.2016

@author: Albert
'''

class CanonicalLexicon(dict):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        
    def append(self, key , value):
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]
        
    