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
    logging.basicConfig(filename='../res/dev_a1.log', level=logging.DEBUG)
    parser = PLTAGParser("Ich liebe dieses Land sehr.")
    # log1 : 0.41s with only substitution - also malformed trees <-- fix with setting isCurrentRoot - nope asynchron
    # log2 : 0.53s with substitution - now working
    # log3 : 0.84s with substitution and adjunction up
    # log4 : 29.22s with substitution and adjunction! -- implement Test and check specification - then implement prediction