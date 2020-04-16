#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:55:13 2017

@author: hcorrada
"""

def _jaccard_similarity(s1, s2):
    intersect = s1.intersection(s2)
    union = s1.union(s2)
    jaccard_similarity = len(intersect)/len(union)
#    intersect = 0 # This variable holds the number of values that insersect between the two sets.
#    for i in s1:
#        if i in s2:
#            intersect = intersect + 1 # Loop through all values in the first set (s1) and see if they are in the second set (s2), #if so increment by 1.
#    newSet = set(s1 + s2) # add the two sets together and return only the unique values.
#    jaccard_similarlity = (intersect/len(newSet)) # calculate jaccard similarity by diving the number of values that intersected #by the total number of unique values in both sets)
    return jaccard_similarity

class Jaccard:
    def __init__(self):
        self._jaccard_dict = None
        
    def compute_similarity(self, shingled_data, docids=None):
        if docids is not None:
            shingled_data = [x for x in shingled_data if x[0] in docids]
        
        ndocs = len(shingled_data)
        self._jaccard_dict = dict()
        
        for i in range(ndocs-1):
            for j in range(i+1, ndocs):
                (doci, si) = shingled_data[i]
                (docj, sj) = shingled_data[j]
                
                key = tuple(sorted((doci, docj)))
                js = _jaccard_similarity(si, sj)
                self._jaccard_dict[key] = js
        
    def get_similarity(self, doci, docj):
        key = tuple(sorted((doci, docj)))
        return self._jaccard_dict[key]