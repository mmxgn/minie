#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 16:05:31 2018

@author: Emmanouil Theofanis Chourdakis <e.t.chourdakis@qmul.ac.uk>

A python wrapper for MinIE
"""

import os
from jnius import autoclass

class AnnotatedProposition:
    def __init__(self, prop):
        self.java_obj = prop
        
    def __str__(self):
        return self.java_obj.toString()
    
    @property
    def subject(self):
        return self.java_obj.triple.get(0).toString()
    
    @property
    def object(self):
        return self.java_obj.triple.get(2).toString()
    
    @property
    def relation(self):
        return self.java_obj.triple.get(1).toString()
    
    @property
    def triple(self):
        return tuple([self.java_obj.triple.get(n).toString() \
                      for n in range(self.java_obj.triple.size())])

class MinIE:
    def __init__(self):

                
        # Import jnius.autoclass after modifying CLASSPATH
        from jnius import autoclass
        MinIE.autoclass = autoclass
                     
        CoreNLPUtils = autoclass('de.uni_mannheim.utils.coreNLP.CoreNLPUtils')
            
        # Dependency parsing pipeline initialization
        self.parser = CoreNLPUtils.StanfordDepNNParser()
    
    def get_propositions(self,sentence, mode = 'SAFE'):
        """ returns a list of proposition extracted from sentence """
        
        String = autoclass('java.lang.String')            
        
        
        if mode == 'AGGRESSIVE':
            nmode = 0
        elif mode == 'DICTIONARY':
            nmode = 1
        elif mode == 'SAFE':
            nmode = 2
        elif mode == 'COMPLETE':
            nmode = 3
        
        MinIE = autoclass('de.uni_mannheim.minie.MinIE')
        
        self.minie_obj = MinIE(String(sentence), self.parser, nmode)
        
        propositions = [
                AnnotatedProposition(prop) for prop in self.minie_obj.getPropositions().elements()
                if prop is not None ]
        
        return propositions                 


if __name__ == "__main__":
 
    sentence = 'The Joker believes that the hero Batman was not actually born in foggy Gotham City.'
    print("Original sentence:")
    print('\t{}'.format(sentence))
    # Extract triples
    
    # Get MinIE instance
    minie = MinIE()
    
    # Get proposition triples
    triples = [p.triple for p in minie.get_propositions(sentence)]
    
    # Print them
    print("Extracted triples:")
    for t in triples:
        print("\t{}".format(t))