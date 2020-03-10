#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 07:51:26 2017

@author: hcorrada
"""

from plagiarism_lib.article_db import ArticleDB
from plagiarism_lib.minhash import MinHash
from plagiarism_lib.lsh import LSH

import pandas as pd
import numpy as np

def _read_truthfile(filepath):
    with open(filepath, 'r') as f:
        truth_pairs = [tuple(sorted(line.strip().split()))
                       for line in f]
    return set(truth_pairs)

def _get_stats(candidate_pairs, truth_pairs):
    tp = len(candidate_pairs.intersection(truth_pairs))    
    prec = 1.0 * tp / len(candidate_pairs)
    rec = 1.0 * tp / len(truth_pairs)
    print ("  returned: %d, tp=%.4f, prec=%.4f, rec=%.4f" % (len(candidate_pairs), tp, prec, rec))
    return prec, rec

def run(mh, truthfile, ts):
    truth_pairs = _read_truthfile(truthfile)
    
    prec_series = []
    rec_series = []
    
    for t in ts:
        print("Doing LSH with t=", t)        
        lsh = LSH(t)
        lsh.do_lsh(mh)
        
        candidate_pairs = set(lsh.get_candidates())
        prec, rec = _get_stats(candidate_pairs, truth_pairs)        
        prec_series.append(prec)
        rec_series.append(rec)
        
    exp_df = pd.DataFrame({'t': ts, 'prec': prec_series, 'rec': rec_series})
    
    return exp_df