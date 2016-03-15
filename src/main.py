# -*- coding: utf-8 -*-
"""
Created on 04.01.2016

@author: Albert
"""
from PLTAGParser import PLTAGParser
import logging

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = PLTAGParser("Ich liebe dieses Land sehr.")