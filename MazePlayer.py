#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 14:22:00 2017

@author: que

Player for recorded Maze simulations
"""

from tkinter import *
from tkinter import messagebox, filedialog
import os.path
from Maze import CellType, Maze
from MazeView import MazeView

import Rat

import time
import math



    


class MazePlayer(object):
    
    def __init__(self):
        self.master = Tk()
         
        self.file_frame = Frame(self.master)
        Label(self.file_frame,text="Maze file:").pack(side=LEFT)
        self.file_entry = Entry( self.file_frame)
        self.file_entry.pack(side=LEFT)
        Button(self.file_frame, text="Open...", command=self.openFile).pack(side=LEFT)
        Button(self.file_frame, text="Play", command=self.play).pack(side=LEFT)
        self.file_frame.pack(anchor=W)
        
        
        self.maze = None
        self.maze_view = None
        
       
        mainloop()
    
    def openFile( self ):
        """
        When the "open file" button is clicked
        """
        maze_file = filedialog.askopenfilename(defaultextension="*.npy", parent=self.master, title="Open Maze file")
       
        if not maze_file:
            return
        
        if self.maze_view:
            self.maze_view.remove()
        
        self.file_entry.delete(0,END)
        self.file_entry.insert(0,maze_file)
        self.maze = Maze( filename=maze_file)
        self.maze_view = MazeView( self.maze, 30, self.master)
        self.maze_view.drawMaze()  
         
        self.maze_file_name = maze_file
    
    def play( self ):
        """
        Play the saved steps of the current maze file
        """
        step_file_name = os.path.splitext(self.maze_file_name)[0] + '.stp'
        try:
            self.maze.playSavedSteps(step_file_name, 0.05)
        except FileNotFoundError:
            messagebox.showerror('No step file',"There is not step file associated with maze\n{0}".format
                                 (self.maze_file_name))



if __name__ == '__main__':
    me = MazePlayer()