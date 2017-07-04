#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:55:21 2017

Low level Maze Class -
    Handles keeping track of the cells
    
    Maze is stored as a 2D Numpy array of CellType enums. 0 is empty, 1 is a wall, 2 is the start,
    3 is the destination etc.

@author: que
"""

import numpy
from enum import Enum
import time

import Rat
import math
import pickle


MAX_STEPS_MULTIPLIER = 3    # Rat starves after trying more than 3x the numer of cells
MAX_STEPS_STUCK = 3         # Rat caught if stuck in the same cell for more than three times


class RatStarved(Exception):
    """
    Rat took more than 10x the number of cells in the maze to reach the destination and 
    starved to death
    """
    def _init__(self, message):
        self.message = message

class RatStuck(Exception):
    """
    Rat was caught by the cat since it was stuck in the same cell for 3 steps
    """
    
    def _init__(self, message):
        self.message = message

class MazeConfig(Exception):
    """
    Some issue with the maze configuration, no start or destination or no rats added
    """
    pass



class CellType(Enum):
    SPACE=0
    WALL=1
    START=2
    DESTINATION=3
    
class UpdateType(Enum):
    DIRECTION =0
    LOCATION=1
    EVERYTHING=2
    
    
class LocationInfo(object):
    """
    Encapsulates the environment around a maze position. There are several properties which 
    can be queried to find out the type of cell:
        
        front - the type of cell directly in front of the rat
        left  - the type of the cell to the left
        right - the type of cell behind the rat
        behind - the type of cell directly behind the rat
    """
   

   
    def __init__(self, maze, current_location, direction):
       """
       Given a maze and the current location and the direction we are pointing
       the populate the front_wall, left_wall, right_wall and behind_wall properties 
       booleans to indicate if a wall is present
       
       maze - reference to a Maze object
       current_location - a tuple givin the index into the maze object (i,j)
       direction - the direction we are pointing.
       
       
       Available properrties:
           front_loc, left_loc, right_loc, behind_loc - Tuples representing cell positions
            for the front, left, right and behind cell
           front_wall, left_wall, right_wall, behind_wall - Booleans indicating if a wall is
            to the front, left, right or behind the current cell. 
       """
       
       dir_front = math.radians(direction)
       dir_right = math.radians(direction+90)
       dir_behind = math.radians(direction+180)
       dir_left = math.radians(direction+270)
       
       self.front_loc = (current_location[0]+int(math.sin(dir_front)),
                                     current_location[1]+int(math.cos(dir_front)))      
       self.front_wall = maze.getCellTypeByLocation(self.front_loc)==CellType.WALL
       
 
       self.left_loc = (current_location[0]+int(math.sin(dir_left)),
                                     current_location[1]+int(math.cos(dir_left)))      
       self.left_wall = maze.getCellTypeByLocation(self.left_loc)==CellType.WALL
 
       self.right_loc = (current_location[0]+int(math.sin(dir_right)),
                                     current_location[1]+int(math.cos(dir_right)))      
       self.right_wall = maze.getCellTypeByLocation(self.right_loc)==CellType.WALL
 
 
       self.behind_loc = (current_location[0]+int(math.sin(dir_behind)),
                                     current_location[1]+int(math.cos(dir_behind)))      
       self.behind_wall = maze.getCellTypeByLocation(self.behind_loc)==CellType.WALL
 



class Maze(object):
    """
    Basic Maze Object - defines the spaces and walls. Each maze is a 2D array of cells. Each cell
    is either an empty space, a wall or the destination
    
    
    """
    
    def __init__( self, width=1, height=1, filename=None):
        """
        width: An integer representing how many cells wide the maze is
        height: An integer representing how many cells high the maze is
        """
        
        if filename:
            self.readFromFile(filename)
        else:
            self.maze_array = numpy.full((width,height), CellType.SPACE, dtype = CellType)
        
 
        self.setBorders()
        self.views = []
        self.rats = []
        self.start = None
        self.destination = None
        self.num_steps = 0
        self.step_delay = 0
        self.steps = []
        
        try: 
            self.getDestination()
            self.getStart()
        except MazeConfig:
            pass
        
        
    def setBorders( self ):
        """
        All mazes need a boarder of walls around the perimeter. This method
        adds walls for all around the edge.
        """
        self.maze_array[:,0] = CellType.WALL
        self.maze_array[0,:] = CellType.WALL

        self.maze_array[self.getWidth()-1,:] = CellType.WALL
        self.maze_array[:,self.getHeight()-1] = CellType.WALL
        
    def onBorder( self, loc):
        """
        Returns true if the specified location is on a border cell
        """
        if loc[0] == 0:
            return True
            
        if loc[1] == 0:
            return True
        
        if loc[0] == self.getWidth() -1:
            return True
        
        if loc[1] == self.getHeight() -1:
            return True
            
    
        
    def getCellType(self,x,y):
        return self.maze_array[x,y]
    
    def getCellTypeByLocation( self, loc):
        """
        loc is an (i,j) tuple
        """
        return self.maze_array[loc[0],loc[1]]
    
    def setCellType( self, x, y, cell_type):
        
        # We should only have a single destination or start. So for each one of these 
        # make sure we convert the current destination or start into a space
        if cell_type == CellType.START:
            if self.hasStart():
                st= self.getStart()
                self.maze_array[st[0],st[1]] = CellType.SPACE
            self.start=(x,y)
        if cell_type == CellType.DESTINATION:
            if self.hasDestination():
                dt= self.getDestination()
                self.maze_array[dt[0],dt[1]] = CellType.SPACE
            self.destination=(x,y)
        
        
        self.maze_array[x,y] = cell_type
    
    def writeToFile( self, filename ):
        """
        Write to Numpy formatted file
        """
        numpy.save(filename, self.maze_array)
    
    def readFromFile( self, filename ):
        """
        Read from Numpy formatted file
        """
        self.maze_array = numpy.load(filename)
        
    def reset(self):
        """
        Remove all rates and reset for the next simulation
        """
        self.num_steps =0
        self.rats=[]
        
    def saveSteps( self, filename):
        """
        Save the steps used for solving the maze to a pickled file
        """
        f = open(filename,'wb')
        pickle.dump(self.steps, f)
        f.close()
        
    def playSavedSteps(self, filename, step_delay=0.0):
        """
        Play the saved steps
        """
        
        f=open(filename, 'rb')
        self.steps = pickle.load(f)
        f.close()
        
        
        self.rats = []
        
        # At a rat for each item of the lists in the first element of steps
        num_rats = len(self.steps[0][0])
        for irat in range(num_rats):
            self.addRat(Rat.DumbRat())
        
        self.updateViews(UpdateType.EVERYTHING)
            
        for step in self.steps:
           
            for irat,rat in enumerate(self.rats):
                rat.setDirection(step[0][irat])
                
            self.updateViews(UpdateType.DIRECTION) 
            time.sleep(step_delay)
            
            
            for irat,rat in enumerate(self.rats):
                rat.setLocation(step[1][irat])  # Second element of steps is the location
               
            self.num_steps += 1
            self.updateViews(UpdateType.LOCATION) 
            time.sleep(step_delay)
                
        
    def getWidth(self):
        return self.maze_array.shape[0]
    
    def getHeight(self):
        return self.maze_array.shape[1]
    
    def addView( self, view ):
        self.views.append(view)
        
    def updateViews( self, update_type):
        
        if update_type == UpdateType.DIRECTION:
            for v in self.views:
                v.updateDirection()
                
        if update_type == UpdateType.LOCATION:
            for v in self.views:
                v.updateLocation()
                
        if update_type == UpdateType.EVERYTHING:
            for v in self.views:
                v.drawMaze()
     
        
    def getNumberSteps(self):
        """
        Return the number of steps performed so far in the maze simulation
        """
        return self.num_steps
        
    
    def hasDestination(self):
        """
        Returns true if  the destination has been set
        """
        return self.destination != None
    
    def hasStart(self):
        """
        Returns true if the start has been set
        """
        return self.start != None
        
        
    def getDestination(self):
        """
        Return the saved destination location if we have it. Otherwise:
             
        Search all maze cells looking for a destination. When it find it return 
        a position (x,y) in terms of array indices:
        """
        
        if self.destination:
            return self.destination
        
        for i in range(self.maze_array.shape[0]):
            for j in range(self.maze_array.shape[1]):
                if self.maze_array[i,j] == CellType.DESTINATION:
                    self.destination = (i,j)
                    return self.destination
                
        if not self.destination:
            raise MazeConfig("Destination was not set for maze")
    
    def getStart(self):
        """
        Return the saved start location if we have it. Otherwise:
             
        Search all maze cells looking for a start. When it find it return 
        a position (x,y) in terms of array indices:
        """
        
        if self.start:
            return self.start
        
        for i in range(self.maze_array.shape[0]):
            for j in range(self.maze_array.shape[1]):
                if self.maze_array[i,j] == CellType.START:
                    self.start = (i,j)
                    return self.start
                
        if not self.destination:
            raise MazeConfig("Start was not set for maze")
        
        
        
    def addRat( self, rat ):
        """
        Add a rat to the list of known rats in the maze
        """
        rat.setLocation(self.getStart())
        self.rats.append(rat)
        
    def getRats( self ):
        """
        Returns the list of rats
        """
        return self.rats
        

    def doStep( self ):
        """
        Do a single step of the Maze simulation. Allow all rats the chance to update their
        direction and then move the rat one step. Returns true if the destination has been 
        reached by any rat
        """
      
        step_dir= []  # Direction per rat for this step
        step_pos = [] # Position per rat for this step
        
        for rat in self.rats:
            loc = LocationInfo( self, rat.getLocation(), rat.getDirection())
            rat.doTurn(loc)
            step_dir.append(rat.getDirection())
        
        self.updateViews(UpdateType.DIRECTION)
        time.sleep(self.step_delay)
        
        for rat in self.rats:
            loc = LocationInfo( self, rat.getLocation(), rat.getDirection())
            
            # Move in front if it's not a wall
            if not loc.front_wall:
                rat.setLocation(loc.front_loc)
            else:
                # If in front of a wall then set the current location so we count that we
                # are stuck:
                rat.setLocation(rat.getLocation()) 
         
            if rat.getNumSameLocation() >= MAX_STEPS_STUCK:
                raise RatStuck("The rat was stuck in the maze and caught by a cat!")
            
            rat_loc = rat.getLocation()
            step_pos.append(rat_loc)
            if rat_loc == self.getDestination():
                return True
            
        self.updateViews(UpdateType.LOCATION)
        time.sleep(self.step_delay)
        
        
        self.steps.append((step_dir,step_pos))
        return False
        
        


    def run( self, step_delay=0 ):
        """
        Run the maze simulation. At most 3x the number of cells steps will be run, more than that
        and the rat dies of starvation. If the rat is stuck in the same cell for 3 steps then it gets
        caught by the cat.
        
        step_delay is the time in seconds we will wait after each turn and each move. This is useful
        when viewing the maze
        
        Pre-conditions:
        The maze must be initialised, usually read from a file. There must be a single start and
        destination cell.
        
        At least one rat must have been added to the maze.
        
        
        Return:
            The number of steps required to reach the destination
        or
            Exceptions:
                RatCaught  - the rat was stuck in the same cell for three steps
                RatStarved - the rat took more than 10x the number of cells to each the destination
        
        """
        
        self.step_delay = step_delay
        
        if len(self.rats) == 0:
            raise MazeConfig("No rats have been added to the maze")
            
        # Check we have a destination:
        dest = self.getDestination()
        
    
        max_steps = MAX_STEPS_MULTIPLIER * self.maze_array.shape[0] * self.maze_array.shape[1]
       
        
        self.steps = []
        for istep in range(max_steps):
            self.num_steps += 1
            if self.doStep():
                return self.num_steps   # Reached the destination
       
        
        
        raise RatStarved("Max number of steps {0} exceeded - rat starved!".format(max_steps))
        
        
            
        
        


def testMaze():

    MAZE_WIDTH=10
    MAZE_HEIGHT=15
    DEST_X = MAZE_WIDTH-2
    DEST_Y = MAZE_HEIGHT-2
    START_X = 1
    START_Y = 1
    print("Testing maze")
    TEST_FILE = "test.npy"
    m = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    assert(m)
    assert(m.getHeight() == MAZE_HEIGHT)
    assert(m.getWidth() == MAZE_WIDTH )
    assert(m.getCellType(0,0) == CellType.WALL )
    assert(m.getCellType(0,MAZE_HEIGHT-1) == CellType.WALL )
    assert(m.getCellType(MAZE_WIDTH-1,MAZE_HEIGHT-1) == CellType.WALL )
    assert(m.getCellType(MAZE_WIDTH-1,0) == CellType.WALL )
    assert(m.getCellType(MAZE_WIDTH//2,MAZE_HEIGHT//2) == CellType.SPACE )

    assert(m.onBorder((0,0)))
    assert(m.onBorder((0,5)))
    assert(m.onBorder((MAZE_WIDTH-1,0)))
    assert(m.onBorder((MAZE_WIDTH-1,MAZE_HEIGHT-1)))

    assert(not m.hasStart())
    assert(not m.hasDestination())
 
    m.setCellType(DEST_X, DEST_Y, CellType.DESTINATION)
    assert(m.getCellType(DEST_X,DEST_Y) == CellType.DESTINATION)
    
    
    dest = m.getDestination()
    assert( dest == (DEST_X,DEST_Y))
    
    # Check we only have one destination at any time:
    m.setCellType(DEST_X-1, DEST_Y-1, CellType.DESTINATION)
    assert(m.getCellType(DEST_X-1,DEST_Y-1) == CellType.DESTINATION)
    assert(m.getCellType(DEST_X,DEST_Y) == CellType.SPACE)
    m.setCellType(DEST_X, DEST_Y, CellType.DESTINATION)
    
    
    m.setCellType(START_X, START_Y, CellType.START)
    assert(m.getCellType(START_X,START_Y) == CellType.START)

    start = m.getStart()
    assert( start == (START_X,START_Y))
  
    assert( m.hasStart())
    assert( m.hasDestination())
    
    m.writeToFile(TEST_FILE)
    
    new_maze = Maze(filename=TEST_FILE)
  
    new_maze.readFromFile(TEST_FILE)
    assert(new_maze.getCellType(0,0) == CellType.WALL )
    assert(new_maze.getCellType(DEST_X,DEST_Y) == CellType.DESTINATION)
    
    dumb_rat= Rat.DumbRat()
    new_maze.addRat(dumb_rat)
    
    
    loc = LocationInfo( new_maze, (START_X,START_Y), 0) 
    assert( not loc.front_wall)
    assert( loc.left_wall )
    assert( not loc.right_wall) 
    assert( loc.behind_wall)
   
    loc = LocationInfo( new_maze, (START_X,START_Y), 90) 
    assert( not loc.front_wall )
    assert( not loc.left_wall)
    assert( loc.right_wall )
    assert( loc.behind_wall)
    
    loc = LocationInfo( new_maze, (START_X,START_Y), 180) 
    assert( loc.front_wall )
    assert( not loc.left_wall )
    assert( loc.right_wall ) 
    assert( not loc.behind_wall) 
    
   
    loc = LocationInfo( new_maze, (START_X,START_Y), 270) 
    assert( loc.front_wall)
    assert( loc.left_wall)
    assert( not loc.right_wall)
    assert( not loc.behind_wall)
    
    
    try:
        new_maze.run()
    except RatStuck:
        pass
  
    print("All Tests Passed")


if __name__ == '__main__':
    testMaze()