#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 07:57:58 2017

@author: que

Collects and displays statistics on runs of the Maze.

Useful for testing Rats which have a stochastic component to their movement

"""

import Maze
from Maze import Maze,RatStuck, RatStarved
import Rat
import numpy as np
import pylab


def run_maze_trials( num_trials, maze_file_name, rat_type, num_rats=1 ):
    """
    Run "num_rats" rats of "rat_type" in the maze given by "maze_file_name" for "num_trials" times
    
    Print the following statistics:
        Number of times (and percentage) of times the run succeeded
        Min, Max, Mean and Std Dev of number of steps
        Histogram of number of steps
        
    For the number of steps a histogram will be displayed
    
    A step file which can be played back later will be saved for the minimum number of steps
    found
    
    """
    
    trial_steps = []
    num_succeeded = 0
    num_stuck = 0
    num_starved = 0
    min_steps = None
    
    print("")
    if num_rats == 1:
        print("Running {0} trials on maze in {1} with rat {2}".format( num_trials, maze_file_name, rat_type.__name__))
    else:
        print("Running {0} trials on maze in {1} with {2} rats of type {3}".format( num_trials, maze_file_name,
              num_rats,rat_type.__name__))
   
    print("")
        
        
    for trial in range(num_trials):
        
        if trial and trial % (num_trials//50) == 0:
            print("#",end='')
        maze = Maze(filename=maze_file_name)
        for irat in range(num_rats):
            rat = rat_type()
            maze.addRat(rat)
        
        try:
            num_steps = maze.run()
            num_succeeded += 1
            trial_steps.append(num_steps)
            if min_steps == None or num_steps < min_steps:
                step_filename = os.path.splitext(maze_file_name)[0] + '.stp'
                maze.saveSteps(step_filename)
                min_steps = num_steps
        except RatStuck:
            num_stuck += 1
        except RatStarved:
            num_starved += 1
        
    print("")
    print("")
   
    print("The maze has {0} cells".format( maze.getHeight() * maze.getWidth()))
 
   
    print("  {0} ({1:.1%}) of the trials succeeded".format(num_succeeded, num_succeeded/num_trials))
    print("  In {0} ({1:.1%}) of the trials the rat got stuck".format(num_stuck, num_stuck/num_trials))
    print("  In {0} ({1:.1%}) of the trials the rat starved".format(num_starved, num_starved/num_trials))
    if num_succeeded > 0:
        trials_array = np.array(trial_steps)
        print("")
        print("  Number of steps stats:")
        print("     Minium:        {:5d}".format(min(trials_array)))
        print("     Num with min:  {0:5d}".format(trial_steps.count(min(trials_array))))
        print("     Maximum:       {0:5d}".format(max(trials_array)))
        print("     Mean:          {0:5.1f}".format(np.mean(trials_array)))
        print("     Std Deviation: {0:5.1f}".format(np.std(trials_array)))
        print("     Median:        {0:5.1f}".format(np.median(trials_array)))
    
        pylab.hist(trials_array,bins=50)
        pylab.xlabel("Number of steps to solve maze")
        pylab.ylabel("Number of occurences")
        pylab.title("Histogram of number of steps to solve maze\n {0} with rat {1}"
                    .format(maze_file_name, rat_type.__name__))
        pylab.show()
        
        
if __name__=='__main__':
    
    run_maze_trials(500, 'maze5.npy', Rat.WallFollower, 1)
    