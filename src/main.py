# -*- coding: utf-8 -*-
"""
Created on 16.03.2016

@author: Benjamin Kosmehl
"""
import sys
from os.path import dirname, abspath, join
from TAGSerialParser import TAGSerialParser
sys.path.append(join(dirname(dirname(abspath(__file__))), 'res'))

from PLTAGParser import PLTAGParser
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG) #TODO: move logging config to config file
    logging.basicConfig(filename='../res/dev_a1.log', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(module)-23s(%(levelname)-1s): %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    parser = PLTAGParser("Ich liebe dieses Land sehr.")
    # log1 : 0.41s with only substitution - also malformed trees <-- fix with setting isCurrentRoot - nope asynchronous
    # log2 : 0.53s with substitution - now working
    # log3 : 0.84s with substitution and adjunction up
    # log4 : 29.22s with substitution and adjunction! -- implement Test and check specification - then implement prediction
    # log5 : 8.96s with substitution and adjunction on current and only first fringe of to be integrated
    # log6 : 14.08s with substitution and adjunction on current and only first fringe of to be integrated - stack: 1484
    # log7 : 39.63s same setting as above only move threads so they all be executed at the same time - stack: 1484
    # log8 : 233.39s semi-asynchronous wait - strange - stack: 1484

#    sparser = TAGSerialParser("Ich liebe dieses Land sehr.") # 0.32s correct parse-tree - must be bugged
