#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 07:37:49 2017

@author: hcorrada
"""

import random

# magic constants for perfect hashing of 32-bit integers
DEFAULT_P = 2**33-355
DEFAULT_M = 4294967295

# create a random hash function f(x) = ((ax + b) % p) % m)
# 
# p: prime number, random coefficients generated mod p
# m: range of generated hash numbers, see above
#
# returns:
#   function f
#
# example:
#    f = _make_hash()
#    hash_val = f(100)
def _make_hash(p=DEFAULT_P, m=DEFAULT_M):
    a = random.randint(1, p-1)
    b = random.randint(0, p-1)
    return lambda x: ((a * x + b) % p) % m

# create a list of n random hash functions
#
# n: number of random hash functions to create
# 
# returns:
#    n-long list of random hash functions
#
# example:
#    funcs = _make_hashes(10)
#    hash_vals = [f(x) for f in funcs]
def _make_hashes(n):
    return [_make_hash() for _ in range(n)]


# make a hash function that takes a _vector_ of integers as input
#
# n: length of vectors that will be given as input to hash function
# m: range of generated hash value
#
# returns:
#    function that takes a vector of length n (or shorter) and
#       returns a hash value
#
# example:
#    f = _make_vector_hash(3)
#    hash_val = f([1, 2, 3])
def _make_vector_hash(n, m=DEFAULT_M):
    hfuncs = _make_hashes(n)
    def _f(x):
        acc = 0
        for i in range(len(x)):
            h = hfuncs[i]
            acc += h(x[i])
        return acc % m
    return _f