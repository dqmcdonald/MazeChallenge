#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 11:32:08 2017

@author: que
"""
import random
import numpy as np


def plot_random_dist( num_to_generate):
    """ 
    Plot histogram of random.random()
    """
    
    rands = np.array([random.random() for i in range(num_to_generate)])
    pylab.hist(rands, bins=100, color="orange")
    pylab.title("Distribution of {0:,d} random numbers\nMean = {1:0.6f}".format(
            num_to_generate, rands.mean()))
    pylab.xlabel("Random Number")
    pylab.ylabel("Number of occurances")
    pylab.show()
    
    
    
if __name__=="__main__":
    plot_random_dist(500000)