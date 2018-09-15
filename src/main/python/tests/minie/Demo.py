#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:08:18 2018

@author: Emmanouil Theofanis Chourdakis <e.t.chourdakis@qmul.ac.uk>

This re-implements src/main/java/tests/minie/Demo.java with python
in order to showcase how minie can be used with python.

"""

# Change CLASSPATH to point to the minie jar archive, 
import os
os.environ['CLASSPATH'] = "../../../../../target/minie-0.0.1-SNAPSHOT.jar"

# Uncomment to point to your java home (an example is given for arch linux)
# if you don't have it as an environment variable already.
# os.environ['JAVA_HOME'] = '/usr/lib/jvm/default'

# Import java classes in python with pyjnius' autoclass (might take some time)
from jnius import autoclass

CoreNLPUtils = autoclass('de.uni_mannheim.utils.coreNLP.CoreNLPUtils')
AnnotatedProposition = autoclass('de.uni_mannheim.minie.annotation.AnnotatedProposition')
MinIE = autoclass('de.uni_mannheim.minie.MinIE')
StanfordCoreNLP = autoclass('edu.stanford.nlp.pipeline.StanfordCoreNLP')
String = autoclass('java.lang.String')

# Dependency parsing pipeline initialization
parser = CoreNLPUtils.StanfordDepNNParser()

# Input sentence
sentence = "The Joker believes that the hero Batman was not actually born in foggy Gotham City."

# Generate the extractions (With SAFE mode (mode = 2))
# NOTE: sentence must be wrapped into String, else it won't work.
minie = MinIE(String(sentence), parser, 2)

# Print out the extrations
print("Input sentence:", sentence)
print("=============================")
print("Extractions:")

# getPropositions() below returns an ObjectArrayList. Its elements can be accessed
# as a python list by the .elements() method
for ap in minie.getPropositions().elements():
    
    # Some elements might by null so we don't process them.
    if ap is not None: 
        print("\tTriple:", ap.getTripleAsString())
        print("\tFactuality:", ap.getFactualityAsString())
        if ap.getAttribution().getAttributionPhrase() is not None:
            print("\tAttribution:", ap.getAttribution().toStringCompact());
        else:
            print("\tAttribution: NONE")
        print("\t----------");
        
print("DONE!")