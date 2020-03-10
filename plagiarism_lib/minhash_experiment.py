#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 07:39:02 2017

@author: hcorrada
"""

import pandas as pd
import numpy as np

from plagiarism_lib.jaccard import Jaccard
from plagiarism_lib.minhash import MinHash, invert_shingles

## 
# Create a pandas DataFrame containing exact Jaccard similarities
# between pairs of documents
#
# exp_data: a shingled article dataset
# docids: ids for documents in 'exp_data'
#
# returns: a pandas DataFrame with columns:
#   doci: id of first document
#   docj: id of second document
#   js: Jaccard similarity between pair of documents
def make_js_df(exp_data, docids):
    # create a Jaccard object and compute pairwise similarities
    jacc = Jaccard()
    jacc.compute_similarity(exp_data)

    # create the data frame with all pairwise Jaccard similarities
    ndocs = len(docids)
    doci_series = []
    docj_series = []
    js_series = []
    
    for i in range(ndocs-1):
        for j in range(i+1, ndocs):
            di = docids[i]
            dj = docids[j]
            s = jacc.get_similarity(di, dj)
            doci_series.append(di)
            docj_series.append(dj)
            js_series.append(s)
            
    return pd.DataFrame({'doci': doci_series, 
                         'docj': docj_series, 
                         'js': js_series})


##
# Run an experiment to measure error of MinHash Jaccard similarity estimates
# for various number of hash functions used in MinHash summaries
#
# exp_data: a shingled article dataset
# exp_df: a pandas DataFrame with exact JS computed between pairs of articles 
# hash_vals: number of hash functions to use in the various MinHash JS estimates
#
# side effect: adds columns to exp_df:
#   mh_<k>: Minhash estimate of JS for pair of documents using k hash functions
def run(exp_data, exp_df, hash_vals=[10,20,50,100,1000]):
    
    # invert the shingled articles so we can iterate over
    # shingles 
    inv_data = invert_shingles(exp_data)
    
    # for each of the number of hashes used in experiment
    for num_hash in hash_vals:
        print("Doing minhash for ", num_hash, " hashes")
        
        # compute minhahs signature matrix
        mh = MinHash(num_hash)
        mh.make_matrix(inv_data, inverted=True)
        
        # add the minhash JS estimates for given number of hash functions
        # to experiment dataset
        cur_series = []
        for _, row in exp_df.iterrows():
            s = mh.get_similarity(row['doci'], row['docj'])
            cur_series.append(s)
            
        series_name = 'mh_' + str(num_hash)
        exp_df[series_name] = cur_series
  
# Compute root mean squared error between Minhash estimates and exact JS
# 
# exp_df: pandas DataFrame with exact JS and minhash JS similarities (created by run_mh_exp)
# hash_vals: the hash values used in the various minhash estimates
#
# returns: a pandas DataFrame with columns
#    h: hash value used in minhash estimate
#    rmse: root mean squared error of minhash estimate
def post_process_df(exp_df, hash_vals):
    tmp_df = exp_df
    for num_hash in hash_vals:
        mh_series = 'mh_' + str(num_hash)
        series_name = 'diff_' + str(num_hash)
        tmp_df[series_name] = np.square(exp_df['js'] - exp_df[mh_series])
    
    cols = ['diff_' + str(num_hash) for num_hash in hash_vals]
    mns = tmp_df[cols].mean()
    rmse_df = pd.DataFrame({'h': hash_vals, 'rmse': np.sqrt(mns)})
    return rmse_df
    