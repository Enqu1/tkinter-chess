import tkinter as tk, logic, minigames
from PIL import Image, ImageTk
from tkinter import simpledialog

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

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Chess')
        self.root.resizable(False, False)

        self.board = tk.Frame(self.root, bg = '#001477')
        self.holder = tk.Frame(self.root, width=40, height=16)
        self.init()

    def init(self):
        self.logic = logic.logic(self)
        
        self.notations = ''
        self.FEN = ''
        self.holder.pack()
        self.labels = []

        self.selectedPiece = None
        self.savedX = None
        self.savedY = None

        self.infoHolder = tk.Frame(self.holder, width=30)
        self.infoHolder.columnconfigure(0, weight=1)
        self.infoHolder.columnconfigure(1, weight=1)
        self.infoHolder.grid(column=1, row=0, padx=10, sticky=tk.N, pady=30)

        self.notationButton = tk.Button(self.infoHolder, width=10, text='Notations', command=lambda: self.switch('N'))
        self.notationButton.grid(column=0, row=0, sticky=tk.W)

        self.FENButton = tk.Button(self.infoHolder, width=10, text='FEN', command=lambda: self.switch('F'))
        self.FENButton.grid(column=1, row=0, sticky=tk.W)

        self.notationLabel = tk.Text(self.infoHolder, width=50, height=30, wrap=tk.WORD)
        self.notationLabel.grid(column=0, row=1, pady=30)

        self.FENLabel = tk.Text(self.infoHolder, width=50, height=30)
        self.FENLabel.grid(column=0, row=1, pady=30)

        self.activeInfo = 'N'

        self.menuBar = tk.Menu(self.root)
        self.gameMenu = tk.Menu(self.menuBar, tearoff=0)
        self.gameMenu.add_command(label='Load FEN', command=self.loadFEN)
        self.gameMenu.add_command(label='New Game', command=self.init)

        self.minigamesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.minigamesMenu.add_command(label='Mate in 1', command=lambda: minigames.Minigame('M1'))
        self.minigamesMenu.add_command(label='Find the coordinate', command=lambda: minigames.Minigame('SQ'))

        self.menuBar.add_cascade(label='Game', menu=self.gameMenu)
        self.menuBar.add_cascade(label='Minigames', menu=self.minigamesMenu)

        self.root.config(menu=self.menuBar)

        self.createBoard()

        self.root.mainloop()

    def loadFEN(self):
        fen = simpledialog.askstring(title='Enter FEN', prompt='Please enter the FEN')
        self.logic.loadFEN(fen)
        self.createBoard()

    def switch(self, info):
        self.activeInfo = info
        self.info()

    def info(self):
        self.FEN = self.logic.generateFEN()

        notationLabel = tk.Text(self.infoHolder, width=50, height=30, wrap=tk.WORD)
        notationLabel.insert(tk.INSERT, self.notations)
        notationLabel.config(state=tk.DISABLED)

        FENLabel = tk.Text(self.infoHolder, width=50, height=30, wrap=tk.WORD)
        FENLabel.insert(tk.INSERT, self.FEN)
        FENLabel.config(state=tk.DISABLED)
        
        self.FENLabel.destroy()
        self.notationLabel.destroy()
        self.FENLabel = FENLabel
        self.notationLabel = notationLabel

        self.FENButton['bg'] = 'white'
        self.notationButton['bg'] = 'white'

        if self.activeInfo == 'N':
            self.notationLabel.grid(column=0, row=1, pady=30)
            self.notationButton['bg'] = 'gray'
        elif self.activeInfo == 'F':
            self.FENLabel.grid(column=0, row=1, pady=30)
            self.FENButton['bg'] = 'gray'



    def createBoard(self):
        board = tk.Frame(self.holder, bg='#001477')

        labels = []
        color = color1
        tc = None

        for i in self.logic.board:
            for y, s in enumerate(i):
                for x, c in enumerate(s):
                    if c == '.': c = ''

                    try:
                        image = Image.open(images[c])
                        img = image.resize((82, 78))
                        myImg = ImageTk.PhotoImage(img)
                        label = tk.Label(board, image=myImg, width=82, height=78, bg=color)
                        label.image = myImg
                        label.grid(row=y, column=x, padx=1, pady=1)
                    except Exception as e:
                        label = tk.Label(board, text=c, font=('Arial', 25, 'bold'), width=4, height=2, bg=color, fg=tc)
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
        self.board.grid(column=0, row=0, padx=10, pady=10)

        self.info()

    def click(self, event, ix):
        label = self.labels[ix][0]
        x = self.labels[ix][2]
        y = self.labels[ix][3]   

        if self.selectedPiece != None and self.selectedPiece != label:
            self.logic.play(self.savedX, self.savedY, x, y)

            self.createBoard()

            self.selectedPiece = None
            self.savedX = None
            self.savedY = None
            return

        if self.labels[ix][1] != '':
            if self.logic.turn != self.labels[ix][1].isupper(): return
            self.selectedPiece = label
            self.savedX = x
            self.savedY = y
            label.configure(bg = selectColor)



if __name__ == '__main__':
    App()