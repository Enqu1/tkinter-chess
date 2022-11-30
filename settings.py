import tkinter as tk
import pip

try:
    import customtkinter
except ImportError:
    pip.main(['install', '--user', 'customtkinter'])
    import customtkinter

defaultImages = {
    'b': './Images/default/black/bishop.png',
    'B': './Images/default/white/bishop.png',
    'k': './Images/default/black/king.png',
    'K': './Images/default/white/king.png',
    'n': './Images/default/black/knight.png',
    'N': './Images/default/white/knight.png',
    'p': './Images/default/black/pawn.png',
    'P': './Images/default/white/pawn.png',
    'q': './Images/default/black/queen.png',
    'Q': './Images/default/white/queen.png',
    'r': './Images/default/black/rook.png',
    'R': './Images/default/white/rook.png',
}
fantasyImages = {
    'b': './Images/fantasy/black/bishop.png',
    'B': './Images/fantasy/white/bishop.png',
    'k': './Images/fantasy/black/king.png',
    'K': './Images/fantasy/white/king.png',
    'n': './Images/fantasy/black/knight.png',
    'N': './Images/fantasy/white/knight.png',
    'p': './Images/fantasy/black/pawn.png',
    'P': './Images/fantasy/white/pawn.png',
    'q': './Images/fantasy/black/queen.png',
    'Q': './Images/fantasy/white/queen.png',
    'r': './Images/fantasy/black/rook.png',
    'R': './Images/fantasy/white/rook.png',
}
spatialImages = {
    'b': './Images/spatial/black/bishop.png',
    'B': './Images/spatial/white/bishop.png',
    'k': './Images/spatial/black/king.png',
    'K': './Images/spatial/white/king.png',
    'n': './Images/spatial/black/knight.png',
    'N': './Images/spatial/white/knight.png',
    'p': './Images/spatial/black/pawn.png',
    'P': './Images/spatial/white/pawn.png',
    'q': './Images/spatial/black/queen.png',
    'Q': './Images/spatial/white/queen.png',
    'r': './Images/spatial/black/rook.png',
    'R': './Images/spatial/white/rook.png',
}

class settings:
    def __init__(self, app):
        self.activeTheme = defaultImages
        self.app = app
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('dark-blue')

    def openWindow(self):
        self.root = customtkinter.CTk()
        self.root.title('Settings')
        self.root.resizable(False, False)

        self.title = customtkinter.CTkLabel(master=self.root, text='Settings', text_font=('Arial', 25), pady=10)
        self.title.pack()

        self.a = customtkinter.CTkFrame(master=self.root)
        self.holder = customtkinter.CTkFrame(master=self.a)

        self.themeTextVariable = customtkinter.StringVar(value='Default Theme')

        self.selectTheme = customtkinter.CTkOptionMenu(master=self.holder, values=['Default Theme', 'Fantasy Theme', 'Spatial Theme'],
        command=self.apply, variable=self.themeTextVariable)

        self.selectTheme.grid(row=0, column=0, padx=10, pady=10)

        self.a.pack()
        self.holder.pack(padx=10, pady=10)

        self.root.mainloop()


    def apply(self, _):
        theme = self.themeTextVariable.get()

        if theme == 'Default Theme':
            self.activeTheme = defaultImages
        elif theme == 'Fantasy Theme':
            self.activeTheme = fantasyImages
        else: self.activeTheme = spatialImages

        self.app.createBoard()

