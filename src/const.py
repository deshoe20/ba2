"""
Created on 04.01.2016

@author: Albert
"""

import TAGTree
from nltk.tree import Tree

INPUTSTRING = "UN-Truppen hätten nun in den vier umkämpften Gebieten die Kontrolle übernommen."

OUTTEST = Tree("S", 
               [Tree("NP", 
                     [Tree("NN", 
                           ["UN-Truppen"]
                      )]
                ), Tree("VAFIN", 
                     ["hätten"]
                ), Tree("VP", 
                     [Tree("AVP", 
                           [Tree("ADV", ["nun"])]
                     ), Tree("PP", 
                             [Tree("APPR", ["in"])
                              , Tree("NP", 
                                   [Tree("DP", 
                                         [Tree("ART", ["den"])]
                                         )
                                    , Tree("AP", 
                                         [Tree("CARD", ["vier"])]
                                         )
                                    , Tree("AP", 
                                         [Tree("ADJA", ["umkämpften"])]
                                         )
                                    , Tree("NN", ["Gebieten"])
                                    ])
                             ]                             
                     ), Tree("NP", 
                             [Tree("DP", 
                                   [Tree("ART", ["die"])])
                              , Tree("NN", ["Kontrolle"])]
                     ), Tree("VVPP", ["übernommen"]
                     )]
                )]
               )


