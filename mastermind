from tkinter import *
from tkinter.messagebox import *
import random as r

class Game():
    
    def __init__(self,pegs,colours,attempts):
        
        self.fenetre = Tk(className="Mastermind")
        
        self.Frame1 = Frame(self.fenetre, borderwidth=2, relief=GROOVE, bg="white")
        self.Frame1.pack(fill=BOTH)
        
        self.Frame2 = Frame(self.fenetre, borderwidth=2, relief=GROOVE)
        self.Frame2.pack(padx=10, pady=10)
        
        self.Frame3 = Frame(self.fenetre, borderwidth=2, relief=GROOVE)
        self.Frame3.pack(padx=10, pady=10)
        
        self.reset = Button(self.Frame1, text = "New Game",command=self.restart)
        self.reset.pack(padx=10, pady=10)
        
        self.var = IntVar()
        self.var.set(1)
        self.check = Checkbutton(self.Frame1, text="Allow repetition of colours", variable =self.var)
        self.check.pack()
        
        self.pegs = pegs
        self.colours = colours
        self.attempts = attempts
        
        self.current_row=0
        self.rows = []
        self.attempt=[]
        self.evaluation=[]
        self.solution = []
        self.win = False
        self.combination = self.generate_combination()
        
        self.colour_range = ["yellow", "red", "blue", "green", "purple", "orange", "cyan", "deep pink"][ : self.colours]
        
        self.solution = Row(self, self.pegs, "grey75", False)
        self.solution.pack(anchor = "w")
       
        for i in range(self.attempts):
            a =Row(self, self.pegs, "white", True)
            self.rows.append(a)
            a.pack(side="bottom")
        
        self.cancel = Button(self.Frame3, text = "Cancel", command = self.cancel)
        self.cancel.pack(side="left")
            
        for i in range(len(self.colour_range)) : 
            a = Colour(self, i)
            a.pack(side="left")
        
        self.confirm = Button(self.Frame3, text = "Confirm", command = self.confirm)
        self.confirm.pack(side="left")
            
        self.fenetre.mainloop()
        
    def restart(self):
        self.win = False
        self.current_row = 0
        self.attempt = []
        for i in range(len(self.rows)):
            self.rows[i].default()
        self.solution.default()
        self.combination = self.generate_combination()
            
    def end(self):    
        for i in range(self.pegs):
             self.solution.bigpegs[i].fill(self.colour_range[self.combination[i]])
        if self.win:
            showinfo('You won','You correctly guessed, well done!')
        else:
            showinfo('You lost','You are out of guesses, try again')
            
    def cancel(self):
        row = self.rows[self.current_row]
        if row.current_peg >0:
            row.bigpegs[row.current_peg-1].config(bg="white")
            del(self.attempt[row.current_peg-1])
            row.current_peg-=1
    
    def confirm(self):
        self.evaluate()
        if self.current_row<self.attempts-1 and self.rows[self.current_row].current_peg>0:
            self.current_row+=1
            self.attempt=[]
        elif self.current_row==self.attempts-1 and not self.win:
            self.end()
            
    def generate_combination(self):
        combination = []
        elements = self.pegs
        possibilities = list(range(0, self.colours))
        for i in range(elements):
            a = r.choice(possibilities)
            combination.append(a)
            if self.var.get()==0:
                possibilities.remove(a)
        return combination
    
    def evaluate(self):
        if self.combination==self.attempt:
            self.win=True
            for i in range(self.pegs):
                self.rows[self.current_row].smallpegs[i].fill("red")
            self.end()
        else:
            evaluation = []
            checked_i=[]
            checked_j=[]
            for i in range(len(self.attempt)):
                if self.attempt[i]==self.combination[i]:
                    evaluation.append("red")
                    checked_i.append(i)
            for i in range(len(self.attempt)):
                for j in range(self.pegs):
                    if self.attempt[i]==self.combination[j] and i not in checked_i and j not in checked_j+checked_i:
                        evaluation.append("black")
                        checked_j.append(j)
                        break
            r.shuffle(self.evaluation)
            for i in range(len(evaluation)):
                self.rows[self.current_row].smallpegs[i].fill(evaluation[i])
        
class Colour(Button):
    def __init__(self, game, colour_num):
        
        self.game = game
        self.colour_num= colour_num
        self.colour=self.game.colour_range[self.colour_num]
        
        Button.__init__(self,self.game.Frame3)
        self.config(borderwidth=3,heigh=0,width=2,bg=self.colour,command=self.push)
        
    def push(self):
        row = self.game.rows[self.game.current_row]
        if row.current_peg<self.game.pegs:
            row.bigpegs[row.current_peg].fill(self.colour)
            self.game.attempt.append(self.colour_num)
            row.current_peg+=1
        
class Row(Frame):
    def __init__(self,game, width, bg, complete):
        
        self.game = game
        self.width = width
        self.bg = bg
        self.bigpegs = []
        self.smallpegs = []
        self.complete = complete
        self.current_peg=0
        
        Frame.__init__(self,self.game.Frame2)
        for i in range(self.width):
            a = Case(self, 30 , RIDGE, 4, self.bg)
            self.bigpegs.append(a)
            a.pack(side="left")
         
        if self.complete: 
            for i in range(self.width):
                a = Case(self, 10, GROOVE, 3, self.bg)
                self.smallpegs.append(a)
                a.pack(side="left", padx =3)
    
    def default(self):
        for i in range(self.width):
            if self.complete:
                self.smallpegs[i].config(bg=self.bg)
            self.bigpegs[i].config(bg=self.bg)
        self.current_peg = 0
            
class Case(Frame):
    def __init__(self, row, dim, relief, bw, bg):
        self.row = row
        Frame.__init__(self, self.row)
        self.config(borderwidth=bw,heigh=dim,width=dim,bg =bg, relief=relief)
        
    def fill(self, colour):
        self.config(bg=colour)

def main():
    pegs=int(input("number of pegs: "))
    colours=int(input("number of possible colours (max=8): "))
    attempts=int(input("number of attempts: "))
    a=Game(pegs,colours,attempts)

if __name__== "__main__":
    main()
