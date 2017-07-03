#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 14:22:00 2017

@author: que

Editor for Mazes - allows creation and editing of Mazes
"""

from tkinter import *
from tkinter import messagebox, filedialog
import os.path

from MazeView import MazeView
from Maze import CellType, Maze,RatStuck, RatStarved
import Rat
from PIL import Image, ImageTk
import time
import math


class NewMazeDialog(object):
    """
    Prompts the user for a size and height and creates a new maze
    """
    def __init__(self, maze_editor, parent):
        self.maze_editor = maze_editor
        
        top = self.top = Toplevel(parent)

        Label(top, text="New Maze Dimensions").pack()

        self.width_frame = Frame(self.top)
        Label(self.width_frame,text="Width:").pack(side=LEFT)
        self.width_entry = Entry( self.width_frame)
        self.width_entry.pack(side=LEFT)
        self.width_frame.pack(anchor=W)
        
        self.height_frame = Frame(self.top)
        Label(self.height_frame,text="Height:").pack(side=LEFT)
        self.height_entry = Entry( self.height_frame)
        self.height_entry.pack(side=LEFT)
        self.height_frame.pack(anchor=W)
        
        self.button_frame = Frame(self.top)
        Cancel_Button = Button(self.button_frame,text="Cancel",command=self.cancel).pack(side=RIGHT)
        OK_Button = Button(self.button_frame,text="OK",command=self.ok).pack(side=RIGHT)
        
        self.button_frame.pack(anchor=E)
        
    def ok(self):
        wstr=self.width_entry.get()
        hstr=self.height_entry.get()
        if wstr and hstr:  
            width = int(wstr)
            height = int(hstr)
            self.maze_editor.createNewMaze(width,height)
            
        self.top.destroy()
            
    def cancel(self):
        self.top.destroy()

    


class MazeEditor(object):
    
    def __init__(self):
        self.master = Tk()
         
        self.file_frame = Frame(self.master)
        Label(self.file_frame,text="Maze file:").pack(side=LEFT)
        self.file_entry = Entry( self.file_frame)
        self.file_entry.pack(side=LEFT)
        Button(self.file_frame, text="New...", command=self.newMaze).pack(side=LEFT)
        Button(self.file_frame, text="Open...", command=self.openFile).pack(side=LEFT)
        Button(self.file_frame, text="Save", command=self.writeFile).pack(side=LEFT)
        self.file_frame.pack(anchor=W)
        
        
        self.radio_frame = Frame(self.master)
        self.cell_type = StringVar()
        Radiobutton( self.radio_frame, text="Space", variable=self.cell_type, value="Space").pack(side=LEFT)
        Radiobutton( self.radio_frame, text="Wall", variable=self.cell_type, value="Wall").pack(side=LEFT)
        Radiobutton( self.radio_frame, text="Destination", variable=self.cell_type, value="Destination").pack(side=LEFT)
        Radiobutton( self.radio_frame, text="Start", variable=self.cell_type, value="Start").pack(side=LEFT)
        self.radio_frame.pack(anchor=W)
        
        self.cell_type.set("Space")
        
        self.maze = None
        
        
       
        mainloop()
    
    def openFile( self ):
        """
        When the "open file" button is clicked
        """
        maze_file = filedialog.askopenfilename(defaultextension="*.npy", parent=self.master, title="Open Maze file")
        self.file_entry.delete(0,END)
        self.file_entry.insert(0,maze_file)
        self.maze = Maze( filename=maze_file)
        self.maze.addRat(Rat.DumbRat())
        self.maze_view = MazeView( self.maze, 30, self.master)
        self.maze_view.drawMaze()  
         
        self.maze_view.addCallback(self.clicked)
    
    def writeFile( self ):
        """
        Write the current maze file
        """
        filename=self.file_entry.get()
        if not filename:
            messagebox.showerror(title="No file name", message="There is no filename specified")
            return
       
        
        if not self.maze.hasDestination():
            messagebox.showerror(title="No destination", message="There is no destination for this maze"
                                 "\nPlease set a destination cell and try again")
            return
        
        
        if not self.maze.hasStart():
            messagebox.showerror(title="No start", message="There is no start point for this maze"
                                 "\nPlease set a start cell and try again")
            return


        res = True
        if os.path.exists(filename):
            res = messagebox.askyesno(title="Overwrite file",
                                message="The file {0} already exists - overwrite it?".format(filename))
            
        if res:
            self.maze.writeToFile(filename)
      
    def newMaze(self):
        """
        Prompt the user to the dimensions and create a new maze
        """
        d = NewMazeDialog(self,self.master)
        self.master.wait_window(d.top)
        
    def createNewMaze(self, width, height):
        """
        Create a new maze and display it
        """
        self.maze = Maze(width, height)
        self.maze_view = MazeView(self.maze,30,self.master)
        self.maze_view.drawMaze()
        self.maze_view.addCallback(self.clicked)
    
    def clicked(self, loc):
        """ 
        Handle a click in the maze
        """
        if  self.cell_type.get() == "Space":
            self.maze.setCellType(loc[0], loc[1], CellType.SPACE)
        elif  self.cell_type.get() == "Wall":
            self.maze.setCellType(loc[0], loc[1], CellType.WALL)
        elif  self.cell_type.get() == "Destination":
            self.maze.setCellType(loc[0], loc[1], CellType.DESTINATION)
        elif  self.cell_type.get() == "Start":
            self.maze.setCellType(loc[0], loc[1], CellType.START)
        self.maze_view.drawMaze()




if __name__ == '__main__':
    me = MazeEditor()