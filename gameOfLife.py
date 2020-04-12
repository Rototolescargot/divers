# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:31:27 2020

@author: Marthe
"""

from tkinter import *
from tkinter.messagebox import *

class Game():
    
    def __init__(self,width,length):
        
        self.fenetre = Tk(className="Game of life")
        self.width = width
        self.length = length
        
        self.Frame1 = Frame(self.fenetre, borderwidth=2, relief=GROOVE, bg="grey")
        self.Frame1.pack(fill=BOTH)
        
        self.Frame2 = Frame(self.fenetre, borderwidth=2, relief=GROOVE, bg="grey")
        self.Frame2.pack(fill=BOTH)
        
        self.resetBtn = Button(self.Frame2, text = "Reset",command=self.reset)
        self.resetBtn.pack(side = "left", padx=10, pady=10)
        self.confirm = Button(self.Frame2, text = "Next", command = self.confirm)
        self.confirm.pack(side = "left", padx=10, pady=10)

        self.table = []
        
        for x in range(self.width):
            t = []
            for y in range(self.length):
                a = Cell(self, x, y, RIDGE, 1, "light grey", 1,  False)
                t.append(a)
            self.table.append(t)
        
        self.fenetre.mainloop()
        
    def confirm(self):
        for x in range(self.width):
            for y in range(self.length):
                self.table[x][y].get_neighbours(x, y)
                
        for x in range(self.width):
            for y in range(self.length):
                self.table[x][y].update()
        
    def reset(self):
        self.k = 0
        for x in range(self.width):
            for y in range(self.length):
                self.table[x][y].die()
       
class Cell(Frame):
    
    def __init__(self, game, x, y, relief, dim, bg, bw,  filled):
        self.dim = dim
        self.bw = bw
        self.bg = bg
        self.filled = filled
        self.game = game
        self.x = x
        self.y = y
        Button.__init__(self,self.game.Frame1)
        self.config(borderwidth=bw,heigh=dim,width=dim*2,bg =bg, relief=relief, command=self.live)
        self.grid(row=self.x, column=self.y)
        
    def live(self):
        self.config(bg="black")
        self.filled = True
    
    def die(self):
        self.config(bg="light grey")
        self.filled = False
        
    def update(self):
                
        if (self.nbLiveNeighbours < 2 or self.nbLiveNeighbours > 3) and self.filled:
            self.die()
            
        if (self.nbLiveNeighbours == 3) and not self.filled:
            self.live()
        
        
    def get_neighbours(self, x, y):
        if 0<x<self.game.width -1 and 0<y<self.game.length -1:
            neighbours = [self.game.table[x-1][y-1], self.game.table[x][y-1], 
                    self.game.table[x+1][y-1], self.game.table[x-1][y],
                    self.game.table[x+1][y], self.game.table[x-1][y+1], 
                    self.game.table[x][y+1], self.game.table[x+1][y+1]]
            
        elif x == 0 :
            
            if 0<y<self.game.length - 1:
                neighbours = [self.game.table[x][y-1], self.game.table[x+1][y-1],
                    self.game.table[x+1][y],self.game.table[x][y+1],
                    self.game.table[x+1][y+1]]
                
            elif y == 0:
                neighbours = [self.game.table[x+1][y],self.game.table[x][y+1],
                    self.game.table[x+1][y+1]]
                
            else:
                neighbours = [self.game.table[x][y-1], self.game.table[x+1][y-1],
                    self.game.table[x+1][y]]
                
        elif x == self.game.width-1 :
        
            if 0<y<self.game.length - 1:
                 neighbours = [self.game.table[x-1][y-1], self.game.table[x][y-1], 
                    self.game.table[x-1][y], self.game.table[x-1][y+1], 
                    self.game.table[x][y+1]]
                 
            elif y == 0:
                 neighbours = [self.game.table[x-1][y], self.game.table[x-1][y+1], 
                    self.game.table[x][y+1]]
                 
            else:
                 neighbours = [self.game.table[x-1][y-1], self.game.table[x][y-1], 
                    self.game.table[x-1][y]]
                 
        elif y == 0:
            neighbours = [self.game.table[x-1][y],
                    self.game.table[x+1][y], self.game.table[x-1][y+1], 
                    self.game.table[x][y+1], self.game.table[x+1][y+1]]
            
        else: 
            neighbours = [self.game.table[x-1][y-1], self.game.table[x][y-1], 
                    self.game.table[x+1][y-1], self.game.table[x-1][y],
                    self.game.table[x+1][y]]
         
        self.nbLiveNeighbours=0
        
        for cell in neighbours:
            if cell.filled:
                self.nbLiveNeighbours+=1
            
def main():
    width = 15
    length = 2*width
    Game(width, length)

if __name__== "__main__":
    main()
