import tkinter as tk, logic
from PIL import Image, ImageTk
from tkinter import messagebox
import random

mate1 = ['4k3/8/8/8/1Q5B/4K3/8/8 w - - 0 1#4k3/4Q3/8/8/7B/4K3/8/8 b - - 1 1', '4k3/8/5Q2/8/1B6/4K3/8/8 w - - 0 1#4k3/4Q3/8/8/1B6/4K3/8/8 b - - 1 1', '4k3/1Q6/8/5N2/8/4K3/8/8 w - - 0 1#4k3/4Q3/8/5N2/8/4K3/8/8 b - - 1 1', '4k3/7R/8/6Q1/8/4K3/8/8 w - - 0 1#4k3/4Q2R/8/8/8/4K3/8/8 b - - 1 1']

color1 = '#9ACBFF'
color2 = '#006699'
selectColor = '#B5FFFD'

images = {
    'b': './Images/bb.png',
    'B': './Images/bw.png',
    'k': './Images/kb.png',
    'K': './Images/kw.png',
    'n': './Images/nb.png',
    'N': './Images/nw.png',
    'p': './Images/pb.png',
    'P': './Images/pw.png',
    'q': './Images/qb.png',
    'Q': './Images/qw.png',
    'r': './Images/rb.png',
    'R': './Images/rw.png',
}

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

class Minigame():
    def __init__(self, type):
        self.logic = logic.logic(self)
        self.root = tk.Toplevel()
        self.root.title('Minigame')
        self.root.resizable(False, False)

        self.type = type

        self.notations = ''
        self.FEN = ''
        self.labels = []

        self.holder = tk.Frame(self.root, width=40, height=16)

        self.holder.pack()

        self.selectedPiece = None
        self.savedX = None
        self.savedY = None

        self.board = tk.Frame(self.root)

        if type == 'M1':
            self.root.title('Mate in 1')
            fen = random.choice(mate1).split('#')
            self.logic.loadFEN(fen[0])
            self.targetFEN = fen[1]
            self.remainingMoves = 1
        elif type == 'SQ':
            self.logic.clearBoard()
            self.targetCoord = f'{random.choice(letters)}{random.randint(1, 8)}'
            self.toFind = tk.Label(self.holder, text=f'Coord: {self.targetCoord}', font=('Arial', 15, 'bold'))
            self.toFind.grid(row=0, column=0, padx=10, sticky=tk.W)

        self.drawBoard()

        self.root.mainloop()
    
    def drawBoard(self):
        board = tk.Frame(self.holder, bg='#001477')

        labels = []
        color = color1
        tc = None

        for i in self.logic.board:
            for y, s in enumerate(i):
                for x, c in enumerate(s):
                    if c == '.': c = ''

                    try:
                        img = Image.open(images[c])
                        img = img.resize((41, 39))
                        image = ImageTk.PhotoImage(img)
                        label = tk.Label(board, image=image, width=42, height=40, bg=color)
                        label.image = image
                        label.grid(row=y, column=x, padx=1, pady=1)
                    except Exception as e:
                        label = tk.Label(board, text=c, font=('Arial', 25, 'bold'), width=2, height=1, bg=color, fg=tc)
                        label.grid(row=y, column=x, padx=1, pady=1)

               
                    label.bind('<Button-1>', lambda event, ix = len(labels): self.click(event, ix))

                    if x != 7:
                        if color == color2:
                            color = color1
                        else:
                            color = color2

                    labels.append([label, c, x, y])

        self.board.destroy()
        self.board = board
        self.labels = labels
        self.board.grid(column=0, row=1, padx=10, pady=10)

    def sqareCheck(self, ix):
        coord = f'{letters[ix%8]}{abs(8-ix // 8)}'
        
        if coord == self.targetCoord:
            self.targetCoord = f'{random.choice(letters)}{random.randint(1, 8)}'
            self.toFind.configure(text=f'Coord: {self.targetCoord}')
        else:
            self.root.destroy()
            if messagebox.askyesno(title='Incorrect.', message=f'That was {coord} not {self.targetCoord}\nPlay again?'):
                self.__init__(self.type)

    def click(self, event, ix):
        if self.type == 'SQ':
            self.sqareCheck(ix)
            return

        if self.remainingMoves == 0:
            return

        label = self.labels[ix][0]
        x = self.labels[ix][2]
        y = self.labels[ix][3]   

        if self.selectedPiece != None and self.selectedPiece != label:
            ret = self.logic.play(self.savedX, self.savedY, x, y)
            self.FEN = self.logic.generateFEN()

            self.drawBoard()

            self.selectedPiece = None
            self.savedX = None
            self.savedY = None
            if ret:
                self.remainingMoves -= 1
                if self.remainingMoves == 0:
                    if self.FEN == self.targetFEN:
                        self.root.destroy()
                        if messagebox.askyesno(title='Congratulations', message='You found the checkmate in 1 move!\nPlay again?'):
                            self.__init__(self.type)
                    else:
                        self.root.destroy()
                        if messagebox.askyesno(title='Incorrect.', message='You didn\'t find the checkmate in 1 move.\nPlay again?'):
                            self.__init__(self.type)
        
            return

        if self.labels[ix][1] != '':
            if self.logic.turn != self.labels[ix][1].isupper(): return
            self.selectedPiece = label
            self.savedX = x
            self.savedY = y
            label.configure(bg = selectColor)