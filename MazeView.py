#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 11:10:49 2017

@author: que

A class which represents the Maze as a Tk canvas
"""
from tkinter import *
from tkinter import messagebox

from Maze import CellType, Maze,RatStuck, RatStarved
import Rat
from PIL import Image, ImageTk
import time
import math






class MazeView(object):
    """
    A class which represents the Maze as a Tk canvas
    """
    
    def __init__(self, maze, cell_size, master ):
        """
        Initialise the maze view
        """
        self.maze = maze
        self.cell_size = cell_size
        
        
        self.maze.addView( self )
        
        self.step_label = Label(master, text="")
        self.step_label.pack(fill=X, expand=1)
        self.canvas = Canvas( master, width=maze.getWidth()*cell_size, height=maze.getHeight()*cell_size)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind("<Button-1>", self.buttonCB)
        self.image_table = { }
        self.createRatImages()
        self.callbacks = []
        self.cheese=None
        self.start=None


    def addCallback(self, cb):
        self.callbacks.append(cb)

    def buttonCB( self, event ):
        """
        Registered with the canvas for button one clicks
        """
        location = self.getLocation( (event.x,event.y))
        for c in self.callbacks:
            c(location)
        
    
    
    def createRatImages(self):
        """
        Read and scale images of the rat in all four directions
        """
        
        
        image = Image.open("rat90.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat90_img = image
        self.image_table[90] = photo
       
        
        image = Image.open("rat0.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat0_img = image
        self.image_table[0] = photo
        
        
        image = Image.open("rat270.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat270_img = image
        self.image_table[270]=photo
        
        image = Image.open("rat180.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.rat180_img = image
        self.image_table[180]=photo
        
        image = Image.open("cheese.gif")
        image.thumbnail((self.cell_size*2,self.cell_size*2), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.cheese_img = image
        self.cheese_photo = photo
        
    
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
 
        self.canvas.delete("ALL")
        if self.cheese:
            self.canvas.delete(self.cheese)
        if self.start:
            self.canvas.delete(self.start)
        
        
        for i in range(self.maze.getWidth()):
            for j in range( self.maze.getHeight() ):
                cell_type = self.maze.getCellType(i,j)
                is_start = False
                if cell_type == CellType.SPACE:
                    fill = ""
                elif cell_type == CellType.DESTINATION:
                    dest = (i,j)
                    fill = ""
                elif cell_type == CellType.START:
                    fill = "green"
                    is_start = True
                elif cell_type == CellType.WALL:
                    fill ="black"
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

        
class MazeViewer():
     """
     Displays a maze and allows the running of a simulation
     """
     def __init__(self, filename, rat_type):
         
         self.master = Tk()
         
         self.button = Button(self.master,text="Run", command=self.run)
         self.button.pack()
        
         
         self.maze = Maze(filename=filename)
         rat = rat_type()
         self.maze.addRat(rat)
         self.maze_view = MazeView( self.maze, 30, self.master)
         self.maze_view.drawMaze()  
         

         mainloop()
     
   
        
     def run(self):
        try:
             self.maze.run(0.1)
             messagebox.showinfo('Found!',"The rat found the cheese")
        except RatStuck as e:
            messagebox.showwarning('Stuck',str(e))
        except RatStarved as e:
            messagebox.showwarning('Starved',str(e))


    
if __name__ == '__main__':
    mv = MazeViewer("t2.npy", Rat.TurnLeftRat)