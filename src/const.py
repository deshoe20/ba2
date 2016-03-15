"""
Created on 04.01.2016

@author: Albert
"""

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

    
"""
%%% 18297
prediction:    ADJ    (NP-PD[nom]^null_1 (NP-HD[nom]^1_null* )(NP-AG[gen]^1_1 (DP-NK[gen]^1_null! )(NP-HD[gen]^1_1 )))
Von von    ADJ    (S^null_x (PP-MO^x_x (PP-HD^x_x (PP-HD^x_x (APPR-AC^x_x Von<>))(NP-PC^x_null! ))(APZR-AC^x_null! ))(S-HD^x_null* ))    --    
1953 1953    ARG    (NP-PC^null_x (CARD-NKHD^x_x 1953<>))    --    
an an    ARG    (APZR-AC^null_x an<>)    --    
war sein    ARG    (S-HD^null_x (VP-HD^x_x (VP-HD^x_x (VAFIN-HD^x_x war<>))(NP-SB[nom]^x_null! ))(NP-PD[nom]^x_null! ))    3.sg.past.ind    
er er    ARG    (NP-SB[nom]^null_x (PPER-NKHD^x_x er<>))    3.nom.sg.masc    
Generaldirektor Generaldirektor    ARG    (NP-PD[nom]^null_x (NN-NKHD^x_x Generaldirektor<>))    nom.sg.masc    
des der    ARG    (DP-NK[gen]^null_x (ART-HD^x_x des<>))    gen.sg.neut    
Verteidigungsministeriums Verteidigungsministerium    ADJ    (NP-PD[nom]^null_x (NP-HD[nom]^x_null* )(NP-AG[gen]^x_x (DP-NK[gen]^x_null! )(NP-HD[gen]^x_x (NN-NKHD^x_x Verteidigungsministeriums<>))))    gen.sg.neut    
. .    ADJ    (S-HD^null_x (S^x_null* )($.^x_x .<>))    --    

Von 1953 an war er Generaldirektor des Verteidigungsministeriums .
APPR Von    CARD 1953    APZR an    VAFIN war    PPER er    NN Generaldirektor    ART des    NN Verteidigungsministeriums    $. .
(S (S (PP (PP (PP (APPR Von))(NP (CARD 1953)))(APZR an))(S (VP (VP (VAFIN war))(NP[nom] (PPER er)))(NP[nom] (NP[nom] (NN Generaldirektor))(NP[gen] (DP[gen] (ART des))(NP[gen] (NN Verteidigungsministeriums))))))($. .))
"""  

