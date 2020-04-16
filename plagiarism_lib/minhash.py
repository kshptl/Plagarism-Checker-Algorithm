#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 08:16:15 2017

@author: hcorrada
"""
import numpy as np
from collections import defaultdict
from plagiarism_lib.hashing import _make_hashes

# Invert shingled article dataset so we can iterate over shingles
#
# shingled_data: list of (docid, shingles) tuples
#    docid: document id 
#    shingles: set of 32-bit integers encoding document shingles of corresponding document
#
# returns: sorted list of tuples (s, docid):
#    s: 32-bit integer encoding document shingle
#    docid: id of document where s occurs
def invert_shingles(shingled_data):
    inv_index = []
    docids = []
    
    for (docid, shingles) in shingled_data:
        docids.append(docid)
        for s in shingles:
            item = (s, docid)
            inv_index.append(item)
    return sorted(inv_index), docids


# Create a minhash signature matrix
#
# shingled_data: a shingled article dataset, format depends on argument 'inverted' (see below)
# num_hashes: number of hash functions to use in the minhash summary
# inverted: boolean, is the shingled data already inverted (see below)
#
# returns: tuple (mh, docids) 
#   mh: a numpy matrix (num_hashes x num_docs) of minhash signature
#   docids: a list of document ids
# 
# note: if argument 'inverted' is True, then shingled data is already sorted by shingle, so
# the minhash algorithm can use directly. In this case, 'shingled_data' is assumed to be 
# a sorted list of (s, docid) tuples, with s a shingle, and docid a document id/
#
# If argument 'inverted' is False, then shingled data is organized by document and we need
# to create an inverted index so we can iterate by shingle. In this case 'shingled_data' is
# assumed to be a list of (docid, shingles) tuples with docid a document id and
# shingles a 'set' of shingles
def _make_minhash_sigmatrix(shingled_data, num_hashes, inverted=False):
    
    # invert the shingled data if necessary
    if inverted:
        inv_index, docids = shingled_data
    else:
        inv_index, docids = invert_shingles(shingled_data)
        
    # initialize the signature matrix with infinity in every entry
    num_docs = len(docids)
    sigmat = np.full([num_hashes, num_docs], np.inf)
    
    # create num_hashes random hash functions
    hash_funcs = _make_hashes(num_hashes)
    
    # avoid recomputing hash function values during iteration
    last_s = -1
    hashvals = []
    
    # iterate over shingles 
    for s, docid in inv_index:
        hashvals = [f(s) for f in hash_funcs if s != last_s] # Compute hash functions for the shingle
        last_s = s # update last_s
        
        for idx, new_hash in enumerate(hashvals):
            # get the current hash
            current_hash = sigmat[idx][docids.index(docid)]

            # if the new hash is smaller than the current hash, overwrite it
            sigmat[idx][docids.index(docid)] = new_hash if new_hash < current_hash else current_hash 
            
    #print(s,docid)
    #from pprint import pprint
    #pprint(sigmat)
    return sigmat, docids


# Objects used to create and query minhash summaries
# Example using 10 hash functions:
#   mh = MinHash(10) 
#   mh.make_matrix(article_db)
#   mh.get_similarity(doci, docj)
class MinHash:
    # Construct an empty object that will use 'num_hashes' in the summary
    #
    # num_hashes: number of hashes to use in the 
    def __init__(self, num_hashes):
        self._num_hashes = num_hashes
        self._docids = None
        self._mat = None
        
    # Create the signature matrix
    # 
    # shingled_data: a shingled document dataset (see _make_minhash_sigmatrix)
    # inverted: is the dataset already inverted (see _make_minhash_sigmatrix)
    #
    # side effect: updates self._docids and self._mat atttributes of object
    def make_matrix(self, shingled_data, inverted=False):
        self._mat, self._docids = _make_minhash_sigmatrix(shingled_data,
                                                          self._num_hashes,
                                                          inverted=inverted)
        
    # compute minhash JS estimate for documents di and dj
    #
    # di: id of first document
    # dj: id of second document
    #
    # returns: minhash JS estimate (double)
    def get_similarity(self, di, dj):
        i = self._docids.index(di)
        j = self._docids.index(dj)
        
        # get all the hashes for the two docs into two lists
        hash_i = [row[i] for row in self._mat]
        hash_j = [row[j] for row in self._mat]
        
        # variable to hold the number of hashes that match
        same = 0

        # go through hashes, if any pair are the same increment "same" by 1
        for idx, h in enumerate(hash_i):
            same = same + 1 if hash_i[idx] == hash_j[idx] else same
        
        similarity = same / len(hash_i)
          
        return similarity
    
    def save_matrix(self, file):
        np.save(file, self._mat)
        
    def from_file(self, docids, file):
        self._docids = docids
        self._mat = np.load(file).astype(np.int32)