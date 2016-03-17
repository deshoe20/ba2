# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
"""
import sys
from os.path import dirname, abspath, join
sys.path.append(join(dirname(dirname(abspath(__file__))), 'res'))

from PLTAGParser import PLTAGParser
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = PLTAGParser("Ich liebe dieses Land sehr.") # log : 0.06s with wrongside substitution