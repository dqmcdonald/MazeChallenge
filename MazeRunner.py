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
import MazeView




        
class MazeRunner():
     """
     Displays a maze and allows the running of a simulation
     """
     def __init__(self):
         
        self.master = Tk()
        self.file_frame = Frame(self.master)
        Label(self.file_frame,text="Maze file:").pack(side=LEFT)
        self.file_entry = Entry( self.file_frame)
        self.file_entry.pack(side=LEFT)
        Button(self.file_frame, text="Open...", command=self.openFile).pack(side=LEFT)
        self.run_button = Button(self.file_frame, text="Run", command=self.run)
        self.run_button.pack(side=LEFT)
        self.run_button.config(state=DISABLED)
        self.file_frame.pack(anchor=W)
        
    
        self.rat_type = StringVar(self.master)
        
        rat_types = self.getRatTypes()
        self.rat_type.set(rat_types[0])
        
        self.rat_type_frame = Frame(self.master)
        Label(self.rat_type_frame,text="Rat type:").pack(side=LEFT)
        self.rat_option = OptionMenu(*(self.rat_type_frame, self.rat_type) + tuple(rat_types))
        self.rat_option.pack(side=LEFT)
        self.rat_type_frame.pack(anchor=W)
        
        self.maze=None
        self.maze_view=None
        

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
        self.maze_view = MazeView.MazeView( self.maze, 30, self.master)
        self.maze_view.drawMaze()  
         
        self.maze_file_name = maze_file
        self.run_button.config(state=NORMAL)
        self.step_filename = os.path.splitext(self.maze_file_name)[0] + '.stp'
        
     def run(self):
         
         
        try:
             self.maze.reset()
             rat_class = getattr(Rat,self.rat_type.get())
             rat = rat_class()
             self.maze.addRat(rat)
             self.maze_view.drawMaze()  
             self.maze.run(0.1)
             messagebox.showinfo('Found!',"The rat found the cheese")
             self.maze.saveSteps(self.step_filename)
        except RatStuck as e:
            messagebox.showwarning('Stuck',str(e))
        except RatStarved as e:
            messagebox.showwarning('Starved',str(e))
            
     def getRatTypes(self):
        """
        Open up the Rat module and extract the list of known classes, returning
        it as a list of strings
        """
        ret_list = []
        for name, obj in inspect.getmembers(Rat):
            if inspect.isclass(obj):
                if name != 'ABCMeta' and name != 'RatBase':
                    ret_list.append(name)
        ret_list.sort()
        return ret_list


    
if __name__ == '__main__':
    mr = MazeRunner()