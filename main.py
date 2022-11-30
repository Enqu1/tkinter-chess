import tkinter as tk, logic, minigames, colorLogic, settings
from PIL import Image, ImageTk
from tkinter import simpledialog
import pip

try:
    import customtkinter as ctk
except ImportError:
    pip.main(['install', '--user', 'customtkinter'])
    import customtkinter as ctk

color1 = '#9ACBFF'
color2 = '#006699'
selectColor = '#B5FFFD'



class App:
    def __init__(self):
        self.root = ctk.CTk()
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        self.root.geometry('1100x725')
        self.settings = settings.settings(self)
        self.root.title('Chess')
        self.root.resizable(False, False)

        self.board = ctk.CTkFrame(master=self.root)
        self.holder = ctk.CTkFrame(master=self.root, width=40, height=16)
        self.init()

    def init(self):
        self.logic = logic.logic(self)
        self.colorLogic = colorLogic.logic(self.logic)
        
        self.notations = ''
        self.FEN = ''
        self.holder.pack()
        self.labels = []

        self.selectedPiece = None
        self.savedX = None
        self.savedY = None

        self.infoHolder = ctk.CTkFrame(master=self.holder, width=30)
        self.infoHolder.columnconfigure(0, weight=1)
        self.infoHolder.columnconfigure(1, weight=1)
        self.infoHolder.grid(column=1, row=0, padx=10, sticky=tk.N, pady=30)

        self.notationButton = ctk.CTkLabel(master=self.infoHolder, width=10, text='Notations', text_font=('Arial', 17, 'bold'))
        self.notationButton.grid(column=0, row=0, sticky=tk.W, padx=10, pady=(10, 0))

        self.FENLabel = ctk.CTkLabel(master=self.infoHolder, width=10, text='FEN', text_font=('Arial', 17, 'bold'))
        self.FENLabel.grid(column=0, row=2, sticky=tk.W, pady=(30, 0), padx=10)

        self.notationLabel = ctk.CTkTextbox(master=self.infoHolder, width=50, height=30, wrap=tk.WORD)
        self.notationLabel.grid(column=0, row=1, pady=30, padx=10)

        self.FENTextBox = ctk.CTkTextbox(self.infoHolder, width=50, height=30)
        self.FENTextBox.grid(column=0, row=1, pady=30, padx=10)

        self.activeInfo = 'N'

        self.menuBar = tk.Menu(self.root)
        self.gameMenu = tk.Menu(self.menuBar, tearoff=0)
        self.gameMenu.add_command(label='Load FEN', command=self.loadFEN)
        self.gameMenu.add_command(label='New Game', command=self.init)

        self.minigamesMenu = tk.Menu(self.menuBar, tearoff=0)
        self.minigamesMenu.add_command(label='Mate in 1', command=lambda: minigames.Minigame('M1', self.settings))
        self.minigamesMenu.add_command(label='Find the coordinate', command=lambda: minigames.Minigame('SQ', self.settings))

        self.menuBar.add_cascade(label='Game', menu=self.gameMenu)
        self.menuBar.add_cascade(label='Minigames', menu=self.minigamesMenu)
        self.menuBar.add_command(label='Settings', command=self.settings.openWindow)

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

        notationLabel = ctk.CTkTextbox(self.infoHolder, width=300, height=500, text_font=('Arial', 13, 'bold'), wrap=ctk.WORD)
        notationLabel.insert(ctk.INSERT, self.notations)
        notationLabel.configure(state='disabled')

        FENTextBox = ctk.CTkTextbox(self.infoHolder, width=300, height=30, wrap=tk.NONE)
        FENTextBox.insert(tk.INSERT, self.FEN)
        FENTextBox.configure(state='disabled')
        
        self.FENTextBox.destroy()
        self.notationLabel.destroy()
        self.FENTextBox = FENTextBox
        self.notationLabel = notationLabel

        self.FENTextBox['bg'] = 'white'
        self.notationButton['bg'] = 'white'

        self.notationLabel.grid(column=0, row=1, padx=10)
        self.notationButton['bg'] = 'gray'

        self.FENTextBox.grid(column=0, row=3, pady=(3, 10), padx=10)
        self.FENTextBox['bg'] = 'gray'



    def createBoard(self, colored=None):
        board = tk.Frame(self.holder, bg='#001477')

        if colored != None:
            for i in colored:
                i.grid(column=i[2], row=i[3], padx=1, pady=1)

            return

        labels = []
        color = color1
        tc = None

        for i in self.logic.board:
            for y, s in enumerate(i):
                for x, c in enumerate(s):
                    if c == '.': c = ''

                    try:
                        image = Image.open(self.settings.activeTheme[c])
                        
                        myImg = ImageTk.PhotoImage(image)
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

        for y, row in enumerate(self.logic.board[0]):
            for x, letter in enumerate(row):
                if letter == 'k':
                    if self.logic.bCheck:
                        labels[y*8+x][0]['bg']='red'
                elif letter == 'K':
                    if self.logic.wCheck:
                        labels[y*8+x][0]['bg']='red'

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
            self.colorLogic.colorAvailableSquares(self.labels, ix)



if __name__ == '__main__':
    App()