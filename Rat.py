#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:05:51 2017

@author: que

Rat Module - Handles all classes for Rat behavior in the Maze

"""

from abc import ABCMeta,abstractmethod


import Maze


class RatBase(metaclass=ABCMeta):
    """
    An abstract base class for the Rat behavior. Defines the basic movement
    behavior but can't be directly instantiated, only subclassed
    """
    
    def __init__(self):
        self.direction = 90   # One of 0,90,180,270
        self.location = None
        self.last_location = None
        self.num_same_location = 0
        
        
    def getDirection(self):
        return self.direction
    
    def setDirection(self, direction):
        self.direction=direction

    def turnLeft(self):
        self.direction -= 90
        if self.direction < 0:
            self.direction = 270
    
    def turnRight(self):
        self.direction += 90
        if self.direction >=360 :
            self.direction = 0
            
    def turnAround(self):
        self.direction += 180
        if self.direction > 360:
            self.direction = 90
            
    def setLocation(self, loc):
        if self.last_location == loc:
            self.num_same_location += 1
        else:
            self.num_same_location = 0
        self.last_location = self.location
        self.location=loc
        
    def getLocation(self):
        return self.location
    
    def getNumSameLocation(self):
        return self.num_same_location
    
    def getLastLocation(self):
        return self.last_location
    
    

    
    @abstractmethod
    def doTurn(self, loc_info):
        """ This is the key function for a rat. At each step of the simulation the 
        rat will be able to examine the information in pos_info and have a chance to turn
        before it is moved one cell in the direction it is facing
        """
        pass
    
    
    
    
class DumbRat(RatBase):
    """
    A dumb rat, doesn't actually ever turn
    """
    
    def __init__(self):
        super().__init__()
    
    def doTurn(self, loc_info):
        """
        Dumb rat does nothing - doesn't turn when given the chance
        """
        return 
    

class TurnLeftRat(RatBase):
    """
   This rat always turns left when faced with a wall!
    """
    
    
    
    def doTurn(self, loc_info):
        """
        Always turn left when faced with a wall
        """
        if loc_info.front_wall:
            self.turnLeft()
    



class TurnAroundRat(RatBase):
    """
   This rat always turns around when faced with a wall!
    """
    
 
    
    def doTurn(self, loc_info):
        """
        Always turn around when faced with a wall
        """
        if loc_info.front_wall:
            self.turnAround()
    








def testRat():
    """ Test cases for the rat class"""
    
    print("Testing Rat")
    try:
        base_rat = RatBase()
    except TypeError:
        pass  # Expected, shouldn't be able to instantiate a base rat
        
    
    dr = DumbRat()
    
    
    assert(dr.getDirection() == 90)
    dr.turnLeft();
    assert(dr.getDirection() == 0)
    dr.turnLeft()
    assert(dr.getDirection() == 270)
    dr.turnLeft()
    assert(dr.getDirection() == 180)
    dr.turnLeft()
    assert(dr.getDirection() == 90)
    
    assert(dr.getDirection() == 90)
    dr.turnRight();
    assert(dr.getDirection() == 180)
    dr.turnRight()
    assert(dr.getDirection() == 270)
    dr.turnRight()
    assert(dr.getDirection() == 0)
    dr.turnRight()
    assert(dr.getDirection() == 90)
    
    assert(dr.getDirection() == 90)
    dr.turnAround();
    assert(dr.getDirection() == 270)
    dr.turnRight()
    assert(dr.getDirection() == 0)
    dr.turnAround()
    assert(dr.getDirection() == 180)
    dr.turnRight()
    assert(dr.getDirection() == 270)
    dr.turnAround()
    assert(dr.getDirection() == 90)
    
    print("All tests passed")
    

if __name__ == "__main__":
    testRat()