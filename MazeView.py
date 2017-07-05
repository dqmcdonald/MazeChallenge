#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:10:49 2017

@author: que

A class which represents the Maze as a Tk canvas
"""
from tkinter import *

from tkinter import messagebox, filedialog

from Maze import CellType, Maze,RatStuck, RatStarved
import Rat
from PIL import Image, ImageTk
import time
import math
import os.path
import inspect



class MazeView(object):
    """
    A class which represents the Maze as a Tk canvas
    """
    
    def __init__(self, maze,  master, cell_size=None, show_grid=False ):
        """
        Initialise the maze view
        """
        self.maze = maze
        
        if cell_size is None:
            self.cell_size = self.calculateCellSize(maze)
        else:
            self.cell_size = cell_size
           
            
        
        
        self.show_grid = show_grid
        
        
        self.maze.addView( self )
        
        self.step_label = Label(master, text="")
        self.step_label.pack(fill=X, expand=1)
        self.canvas = Canvas( master, width=maze.getWidth()*self.cell_size, height=maze.getHeight()*self.cell_size)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind("<Button-1>", self.buttonCB)
        self.canvas.bind("<B1-Motion>", self.buttonCB)
        self.image_table = { }
        self.createRatImages()
        self.callbacks = []
        self.cheese=None
        self.start=None


    def addCallback(self, cb):
        self.callbacks.append(cb)

    def buttonCB( self, event ):
        """
        Registered with the canvas for button one clicks and drags
        """
        location = self.getLocation( (event.x,event.y))
        for c in self.callbacks:
            c(location)
        
        
    def calculateCellSize(self, maze):
        """
        Calculate an appropriate cell size based on the maximum dimension of the maze
        """
        max_dim = max(maze.getHeight(), maze.getWidth())
      
        # Apply a hueristic:
        if max_dim <= 20:
            return 40
        if max_dim <= 30:
            return 30
        if max_dim <= 40:
            return 20
        else:
            return 10
    
    
    def createRatImages(self):
        """
        Read and scale images of the rat in all four directions
        """
        
        
        image = Image.open("images/rat90.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat90_img = image
        self.image_table[90] = photo
       
        
        image = Image.open("images/rat0.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat0_img = image
        self.image_table[0] = photo
        
        
        image = Image.open("images/rat270.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat270_img = image
        self.image_table[270]=photo
        
        image = Image.open("images/rat180.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat180_img = image
        self.image_table[180]=photo
        
        image = Image.open("images/cheese.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.cheese_img = image
        self.cheese_photo = photo
      
    
    def remove(self):
        if self.canvas:
            self.canvas.pack_forget()
        if self.step_label:
            self.step_label.pack_forget()
    
    def setCellSize( self, cell_size ):
        """
        Set the size of each cell, with determine the size the maze overall
        """
        self.cell_size = cell_size
    
    def getCoords( self, location ):
        """
        Get the coordinates based on the location
        """
        half_cell = self.cell_size*0.5
        return (location[0]*self.cell_size+half_cell,
                (self.maze.getHeight()-location[1])*self.cell_size-(half_cell))
    
    def getLocation( self, coords):
        """
        Converts coordinates on the canvas into (i,j) location in the maze
        """
        
        i = math.floor(coords[0]/self.cell_size)
        j = self.maze.getHeight() - math.floor(coords[1]/self.cell_size)-1
        return (i,j)
        
    def updateLocation( self ):
        """
        The rat locations have potentially changed - update the images
        """
    
        for rat in self.maze.getRats():
            last_coord = self.getCoords(rat.getLastLocation())
            curr_coord = self.getCoords(rat.getLocation())
            delta_x = curr_coord[0] - last_coord[0]
            delta_y = curr_coord[1] - last_coord[1]
            self.canvas.move( rat.image, delta_x, delta_y)
            
        self.step_label.configure( text = "Step: {0}".format(self.maze.getNumberSteps()))
        self.canvas.update_idletasks()
    
    def updateDirection( self ):
        """
        The rat directions have potentially changed - update the images
        """
        
        
        for rat in self.maze.getRats():
            self.canvas.itemconfig( rat.image, image=self.image_table[rat.getDirection()])
        
    
    def drawMaze( self ):
        """
        Draw the maze() 
        """
        
      
        half_cell = self.cell_size*0.5
        xpos = 0
        ypos = (self.maze.getHeight()-1)*self.cell_size
        dest = (0,0)
        start= (0,0)
 
        self.canvas.delete(ALL)
        if self.cheese:
            self.canvas.delete(self.cheese)
        if self.start:
            self.canvas.delete(self.start)
        
        fill=""
        for i in range(self.maze.getWidth()):
            for j in range( self.maze.getHeight() ):
                cell_type = self.maze.getCellType(i,j)
                is_start = False
                is_space = False
                if cell_type == CellType.SPACE:
                    is_space = True
                    fill = ""
                elif cell_type == CellType.DESTINATION:
                    dest = (i,j)
                    fill = ""
                elif cell_type == CellType.START:
                    fill = "green"
                    is_start = True
                elif cell_type == CellType.WALL:
                    fill ="black"
                    
                if is_space and self.show_grid:
                    rect = self.canvas.create_rectangle(xpos,ypos,xpos+self.cell_size, ypos+self.cell_size, fill=fill)
                
                if not is_space:
                    rect = self.canvas.create_rectangle(xpos,ypos,xpos+self.cell_size, ypos+self.cell_size, fill=fill)
                    
                if is_start:
                    self.start= rect
                
                ypos -= self.cell_size
            xpos += self.cell_size
            ypos = (self.maze.getHeight()-1)*self.cell_size
        
    
        for rat in self.maze.getRats():
            rat_loc = rat.getLocation()
            rat_coord = self.getCoords(rat_loc)
            rat.image = self.canvas.create_image(rat_coord[0],rat_coord[1],
                                            image=self.image_table[90], state=NORMAL)
           
        
        if self.maze.hasDestination() :
            dest = self.maze.getDestination()
            self.cheese = self.canvas.create_image(dest[0]*self.cell_size+half_cell,
                (self.maze.getHeight()-dest[1])*self.cell_size-(half_cell),
                    image=self.cheese_photo, state=NORMAL)

        
