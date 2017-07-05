#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:05:51 2017

@author: que

Rat Module - Handles all classes for Rat behavior in the Maze

"""

from abc import ABCMeta,abstractmethod


import Maze
import random


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
        if self.direction >= 360:
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
        before it is moved one cell in the direction it is facing.
        
        loc_info provides the following information:
            front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
            front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
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
        This is the key function for a rat. At each step of the simulation the 
        rat will be able to examine the information in pos_info and have a chance to turn
        before it is moved one cell in the direction it is facing.
        
        loc_info provides the following information:
            front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
            front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
            destination - the destination cell (i,j) tuple

       
        Dumb rat does nothing - doesn't turn when given the chance
        
        
        """
        
        return 
 
    

class TurnLeftRat(RatBase):
        """
        This rat always turns left when faced with a wall!
        """
    
    
    
        def doTurn(self, loc_info):
            """        
            This is the key function for a rat. At each step of the simulation the 
            rat will be able to examine the information in pos_info and have a chance to turn
            before it is moved one cell in the direction it is facing.
        
            loc_info provides the following information:
                front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
                front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
                destination - the destination cell (i,j) tuple
  
            
            Always turn left when faced with a wall
            """
        
        
            if loc_info.front_wall:
                self.turnLeft()
    



class RandomRat(RatBase):
        """
        This rat makes random turns
        """
    
    
    
        def doTurn(self, loc_info):
            """        
            This is the key function for a rat. At each step of the simulation the 
            rat will be able to examine the information in pos_info and have a chance to turn
            before it is moved one cell in the direction it is facing.
        
            loc_info provides the following information:
                front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
                front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
                destination - the destination cell (i,j) tuple


            """
            r = random.random()        
            if r < 0.05 and not loc_info.left_wall:
                self.turnLeft()
            elif r < 0.10 and not loc_info.right_wall:
                self.turnRight()
            else:
                if loc_info.front_wall:
                    r  =random.random()
                    if r < 0.5 and not loc_info.left_wall:
                        self.turnLeft()
                    else:
                        self.turnRight()
                    
            
            
class SmellingRat(RatBase):
        """
        This rat can smell the cheese and will try and turn towards it
        """
    
        def distanceToDest( self, loc, dest):
            """
            Returns the square of the distance between locations "loc" and "dest"
            """
            xdiff = dest[0] - loc[0]
            ydiff = dest[1] - loc[1]
            return xdiff*xdiff + ydiff*ydiff
    
        def doTurn(self, loc_info):
            """        
            This is the key function for a rat. At each step of the simulation the 
            rat will be able to examine the information in pos_info and have a chance to turn
            before it is moved one cell in the direction it is facing.
        
            loc_info provides the following information:
                front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
                front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
                destination - the destination cell (i,j) tuple


            """
            
            r=random.random()
            
            if r < 0.2:
                # Take a random turn towards the cheese:
                if (self.distanceToDest(loc_info.left_loc,loc_info.destination) <
                        self.distanceToDest(loc_info.right_loc, loc_info.destination) and not
                        loc_info.left_wall):
                    self.turnLeft()
                else:
                    if not loc_info.right_wall:
                            self.turnRight()
                            
            else:
                if loc_info.front_wall:
                    r = random.random()
                    if r < 0.5 and not loc_info.left_wall:
                        self.turnLeft()
                    else:
                        self.turnRight()
                        
class SmellingRat2(RatBase):
        """
        This rat can smell the cheese and will try and turn towards it
        """
    
        def distanceToDest( self, loc, dest):
            """
            Returns the square of the distance between locations "loc" and "dest"
            """
            xdiff = dest[0] - loc[0]
            ydiff = dest[1] - loc[1]
            dist = xdiff*xdiff + ydiff*ydiff
            return dist
    
        def doTurn(self, loc_info):
            """        
            This is the key function for a rat. At each step of the simulation the 
            rat will be able to examine the information in pos_info and have a chance to turn
            before it is moved one cell in the direction it is facing.
        
            loc_info provides the following information:
                front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
                front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
                destination - the destination cell (i,j) tuple


            """
            
            r=random.random()
            
            dist_from_current = self.distanceToDest(self.getLocation(), loc_info.destination)
            dist_from_left = self.distanceToDest(loc_info.left_loc, loc_info.destination)
            dist_from_right = self.distanceToDest(loc_info.right_loc, loc_info.destination)
                
            
            if loc_info.front_wall:
                
                
                if not loc_info.left_wall and (dist_from_left < dist_from_current or r< 0.5):
                    self.turnLeft()
                    return
                if not loc_info.right_wall and (dist_from_right < dist_from_current or r<0.5):
                    self.turnRight()
                    return
                if loc_info.left_wall and loc_info.right_wall:
                    self.turnAround()
                    return
                if not loc_info.left_wall:
                    self.turnLeft()
                    return
                if not loc_info.right_wall:
                    self.turnRight()
                    return
                
            else:
                if not loc_info.left_wall and  (dist_from_left < dist_from_current or r < 0.5):
                        self.turnLeft()
                if not loc_info.right_wall and (dist_from_right < dist_from_current and r < 0.5):
                        self.turnRight
                    
                            
class WallFollower(RatBase):
        """
        This rat follows the right hand rule. Given a choice it will turn right
        """
    
      
    
        def doTurn(self, loc_info):
            """        
            This is the key function for a rat. At each step of the simulation the 
            rat will be able to examine the information in pos_info and have a chance to turn
            before it is moved one cell in the direction it is facing.
        
            loc_info provides the following information:
                front_wall, left_wall, right_wall, behind_wall - return True if there's a wall 
                    in that direction
                front_loc, left_loc, right_lock, behind_loc - return the location (x,y) of those cells
                destination - the destination cell (i,j) tuple


            """
            
            if not loc_info.right_wall:
                self.turnRight()
            elif not loc_info.left_wall and loc_info.front_wall:
                self.turnLeft()
            elif loc_info.right_wall and loc_info.left_wall and loc_info.front_wall:
                self.turnAround()
                



















################ Anything below here is simply testing for the Rat base class


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