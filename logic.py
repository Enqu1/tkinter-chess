class logic:
    def __init__(self, a):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.move = 1
        self.turn = 1

        self.halfMoveClock = 0

        self.enPassentSquare = (None, None)
        self.enPassentThisMove = False

        self.wKingStart = (7, 4)
        self.bKingStart = (0, 4)

        self.wOO = True
        self.wOOO = True
        self.bOO= True
        self.bOOO = True
        
        self.wCheck = False
        self.bCheck = False

        self.app = a

        self.board = [['........'] * 8]
        self.board[0][0] = 'rnbqkbnr'
        self.board[0][1] = 'pppppppp'
        self.board[0][6] = 'PPPPPPPP'
        self.board[0][7] = 'RNBQKBNR'
    

    def loadFEN(self, fen):
        if fen == None: return

        self.__init__(self.app)
        fen = fen.split(' ')
        
        
        board = fen[0].split('/')

        newBoard = [[]]

        for i in board:
            row = ''
            for piece in i:
                try:
                    dots = int(piece)
                    row = row + '.'*dots
                except Exception:
                    row = row + piece
            newBoard[0].append(row)

        self.board = newBoard

        if fen[1] == 'w':
            self.turn = 1
        else:
            self.turn = 0

        self.wOO = False; self.wOOO = False
        self.bOO = False; self.bOOO = False

        for i in fen[2]:
            if i == 'K': self.wOO = True
            if i == 'Q': self.wOOO = True
            if i == 'k': self.bOO = True
            if i == 'q': self.bOOO = True

        if fen[3] == '-':
            self.enPassentSquare = (None, None)
        else:
            ix = self.letters.index(fen[3][0])
            self.enPassentSquare = (ix, abs(int(fen[3][1]) - 8))

        self.halfMoveClock = int(fen[4])
        self.move = int(fen[5])
                    
    def canMove(self, x, y):
        target = self.board[0][y][x]
        if self.turn:
            if target.islower() or target == '.': return True
        else:
            if target.isupper() or target == '.': return True

        return False

    def swap(self, x1, y1, x2, y2):
        pieceText = self.board[0][y1][x1]

        self.board[0][y2] = self.board[0][y2][:x2] + pieceText + self.board[0][y2][x2 + 1:]
        self.board[0][y1] = self.board[0][y1][:x1] + '.' + self.board[0][y1][x1 + 1:]

        if pieceText.upper() == 'P':
            self.halfMoveClock = 0
        
        if self.enPassentThisMove: self.enPassentThisMove = False
        else: self.enPassentSquare = (None, None)

        if self.turn:
            self.turn=0
        else:
            self.move += 1
            self.turn=1

    def canPawn(self, x1, y1, x2, y2):
        if x1 != x2 and x2 not in [x1 - 1, x1 + 1]: return False

        if self.turn:
            if y2 > y1: return False

            if x2 in [x1 - 1, x1 + 1]:
                if y2 == y1 - 1:
                    if self.board[0][y2][x2] != '.':
                        if self.board[0][y2][x2].islower():
                            if y2 == 0: self.board[0][y1] = self.board[0][y1][:x1] + 'Q' + self.board[0][y1][x1 + 1:]
                            return True
                if (x2, y2) == self.enPassentSquare:
                    if self.board[0][y2+1][x2] != '.':
                        if self.board[0][y2+1][x2].islower():
                            if x2 == x1 - 1:
                                self.board[0][y1] = self.board[0][y1][:x1-1] + '.' + self.board[0][y1][x1:]
                            else:
                                self.board[0][y1] = self.board[0][y1][:x1+1] + '.' + self.board[0][y1][x1+2:]

                            if y2 == 0: self.board[0][y1] = self.board[0][y1][:x1] + 'Q' + self.board[0][y1][x1 + 1:]
                            return True

                return False
                            
            if self.board[0][y2][x1] != '.': return False

            if y1 == 6 and y2 == 4:
                if self.board[0][y1-1][x1] != '.': return False
                self.enPassentSquare = (x1, 5)
                self.enPassentThisMove = True
                return True
            if y2 == y1 - 1:
                if y2 == 0: self.board[0][y1] = self.board[0][y1][:x1] + 'Q' + self.board[0][y1][x1 + 1:]
                return True
        else:
            if y1 > y2: return False
            if x2 in [x1 - 1, x1 + 1]:
                if y2 == y1 + 1:
                    if self.board[0][y2][x2] != '.':
                        if self.board[0][y2][x2].isupper():
                            if y2 == 7: self.board[0][y1] = self.board[0][y1][:x1] + 'q' + self.board[0][y1][x1 + 1:]
                            return True
                if (x2, y2) == self.enPassentSquare:
                    if self.board[0][y2-1][x2] != '.':
                        if self.board[0][y2-1][x2].isupper():
                            if x2 == x1 - 1:
                                self.board[0][y1] = self.board[0][y1][:x1-1] + '.' + self.board[0][y1][x1:]
                            else:
                                self.board[0][y1] = self.board[0][y1][:x1+1] + '.' + self.board[0][y1][x1+2:]

                            if y2 == 0: self.board[0][y1] = self.board[0][y1][:x1] + 'q' + self.board[0][y1][x1 + 1:]
                            return True

                return False
                                
            if self.board[0][y2][x1] != '.': return False
            
            if y1 == 1 and y2 == 3:
                if self.board[0][y1+1][x1] != '.': return False
                self.enPassentSquare = (x1, 2)
                self.enPassentThisMove = True
                return True
            if y2 == y1 + 1:
                if y2 == 7: self.board[0][y1] = self.board[0][y1][:x1] + 'q' + self.board[0][y1][x1 + 1:]
                return True

        return False

    def canKnight(self, x1, y1, x2, y2):
        if x2 not in [x1 + 1, x1 - 1, x1 + 2, x1 - 2]: return False
        if y2 not in [y1 + 1, y1 - 1, y1 + 2, y1 - 2]: return False

        if x2 in [x1 + 1, x1 - 1]:
            if y2 not in [y1 + 2, y1 - 2]: return False
        if x2 in [x1 + 2, x1 - 2]:
            if y2 not in [y1 + 1, y1 - 1]: return False

        return True

    def canHor(self, x1, y1, x2, y2):
        if x1 != x2 and y2 != y1: return False

        if x1 == x2:
            step = 1
            if y2 - y1 < 0: step = -1

            for i in range(y1 + step, y2, step):
                if self.board[0][i][x1] != '.': return False

        if y1 == y2:
            step = 1
            if x2 - x1 < 0: step = -1

            for i in range(x1 + step, x2, step):
                if self.board[0][y1][i] != '.': return False

        return True

    def checkDiag(self, x1, y1, x2, y2):
        xStep = 1
        if x2 - x1 < 0: xStep = -1
        yStep = 1
        if y2 - y1 < 0: yStep = -1
        y = y1 + yStep

        for x in range(x1 + xStep, x2, xStep):
            if self.board[0][y][x] != '.': return False

            y += yStep
            if y == y2: break

        return True

    def canDiag(self, x1, y1, x2, y2):
        for i in range(1, 9):
            if x2 == x1+i and y2 == y1+i: return True
            if x2 == x1+i and y2 == y1-i: return True
            if x2 == x1-i and y2 == y1+i: return True
            if x2 == x1-i and y2 == y1-i: return True

        return False

    def castle(self, x1, y1, x2, y2):
        if self.turn:
            if (y1, x1) == self.wKingStart:
                if x2 in [x1 - 2, x1 + 2]:
                    if y2 == y1:
                        if x2 == x1 + 2:
                            if self.wOO:
                                if self.board[0][y1][x1 + 1] == '.' and self.board[0][y1][x1 + 2] == '.' and self.board[0][y1][x1 + 3] == 'R':
                                    self.board[0][y1] = self.board[0][y1][:x1] + '.RK.'
                                    self.wOO = False
                                    self.wOOO = False
                                    self.app.notations = self.app.notations + f' {self.move}. O-O'
                                    self.turn = 0
                                    return True
                        else:
                            if self.wOOO:
                                if self.board[0][y1][x1 - 1] == '.' and self.board[0][y1][x1 - 2] == '.' and self.board[0][y1][x1 - 3] == '.' and self.board[0][y1][x1 - 4] == 'R':
                                    self.board[0][y1] = '..KR.' + self.board[0][y1][x1 + 1:]
                                    self.wOO = False
                                    self.wOOO = False
                                    self.app.notations = self.app.notations + f' {self.move}. O-O-O'
                                    self.turn = 0
                                    return True
        else:
            if (y1, x1) == self.bKingStart:
                if x2 in [x1 - 2, x1 + 2]:
                    if y2 == y1:
                        if x2 == x1 + 2:
                            if self.bOO:
                                if self.board[0][y1][x1 + 1] == '.' and self.board[0][y1][x1 + 2] == '.' and self.board[0][y1][x1 + 3] == 'r':
                                    self.board[0][y1] = self.board[0][y1][:x1] + '.rk.'
                                    self.wOO = False
                                    self.wOOO = False
                                    self.app.notations = self.app.notations + ', O-O\n'
                                    self.turn = 1
                                    self.move += 1
                                    return 
                        else:
                            if self.bOOO:
                                if self.board[0][y1][x1 - 1] == '.' and self.board[0][y1][x1 - 2] == '.' and self.board[0][y1][x1 - 3] == '.' and self.board[0][y1][x1 - 4] == 'r':
                                    self.board[0][y1] = '..kr.' + self.board[0][y1][x1 + 1:]
                                    self.wOO = False
                                    self.wOOO = False
                                    self.app.notations = self.app.notations + ', O-O-O\n'
                                    self.turn = 1
                                    self.move += 1
                                    return True

        return False

    def canKing(self, x1, y1, x2, y2):
        if y2 in [y1+1, y1-1, y1] and x2 in [x1+1, x1-1, x1]:
            if self.turn: self.wOO = False; self.WOOO = False
            else: self.bOO = False; self.bOOO = False
            
            return True
        return False

    def checkRookStart(self, x, y):
        if self.turn:
            if y == 7:
                if x == 0:
                    self.wOOO = False
                elif x == 7: self.wOO = False
        else:
            if y == 0:
                if x == 0:
                    self.bOOO = False
                elif x == 7: self.bOO = False

    def parsePeice(self, x1, y1, x2, y2):
        piece = self.board[0][y1][x1].upper()

        if self.board[0][y1][x1].isupper() != self.turn:
            return False

        if piece == 'P':
            return self.canPawn(x1, y1, x2, y2)
        
        if piece == 'N':
            return self.canKnight(x1, y1, x2, y2)

        if piece == 'R':
            if self.canHor(x1, y1, x2, y2):
                self.checkRookStart(x1, y1)
                return True
            return False

        if piece == 'B':
            if self.canDiag(x1, y1, x2, y2):
                return self.checkDiag(x1, y1, x2, y2)

        if piece == 'Q':
            if self.canHor(x1, y1, x2, y2): return True
            if self.canDiag(x1, y1, x2, y2):
                return self.checkDiag(x1, y1, x2, y2)
        
        if piece == 'K':
            if self.castle(x1, y1, x2, y2):
                return False
            return self.canKing(x1, y1, x2, y2)

        return False

    def notation(self, x1, y1, x2, y2):
        piece = self.board[0][y1][x1].upper()
        string = self.letters[x2]
        taking = self.board[0][y2][x2] != '.'
        row = abs(8 - y2)

        if taking:
            self.halfMoveClock = 0
            string = f'x{string}'
            if piece == 'P':
                string = f'{self.letters[x1]}{string}'

        if piece == 'P':
            if (x2, y2) == self.enPassentSquare:
                string=f'{self.letters[x1]}x{string}'

        if piece != 'P':
            string = f'{piece}{string}'

        if self.turn == 1:
            string = f' {self.move}. {string}{row}'
        else:
            string = f', {string}{row}\n'


        self.app.notations = self.app.notations + string

    def play(self, x1, y1, x2, y2):
        if not self.canMove(x2, y2): return
        if not self.parsePeice(x1, y1, x2, y2): return

        self.halfMoveClock += 1

        if self.board[0][y1][x1].upper() == 'K':
            print('king move')
            if self.check((y2, x2)): return False

        self.notation(x1, y1, x2, y2)
        self.swap(x1, y1, x2, y2)
        self.check()

        return True

    def generateFEN(self):
        fen = ''

        count = 0

        for y in self.board[0]:
            for c in y:
                if c == '.': count += 1; continue

                if count:
                    fen += str(count)
                    count = 0

                fen = fen + c
            
            if count:
                fen += str(count)
                count = 0
            fen += '/'

        fen = fen[:-1]

        if self.turn:
            fen += ' w '
        else:
            fen += ' b '

        if self.wOO and self.wOOO: fen += 'KQ'
        elif self.wOO: fen += 'K'
        elif self.wOOO: fen += 'Q'

        if self.bOO and self.bOOO: fen += 'kq'
        elif self.bOO: fen += 'k'
        elif self.bOOO: fen += 'q'

        if not self.wOO and not self.wOOO and not self.bOO and not self.bOOO: fen += '-'

        enPassent = '-'

        if self.enPassentSquare[0] != None:
            letter = self.letters[self.enPassentSquare[0]]
            enPassent = f'{letter}{abs(8 - self.enPassentSquare[1])}'

        fen += f' {enPassent} {self.halfMoveClock} {self.move}'

        return fen

    def clearBoard(self):
        self.board = [['........'] * 8]

    def checkPawnAttacks(self, x, y, coords):
        piece = self.board[0][y][x]

        if piece.isupper():
            if y-1 < 0: return
            if x-1 < 0: return
            if x+1 > 7: return

            if self.board[0][y-1][x-1] == 'k': self.bCheck = True
            if self.board[0][y-1][x+1] == 'k': self.bCheck = True
        else:
            if y+1 > 7: return
            if x-1 < 0: return
            if x+1 > 7: return

            if self.board[0][y+1][x-1] == 'K': self.wCheck = True
            if self.board[0][y+1][x+1] == 'K': self.wCheck = True

    def checkHorAttacks(self, x, y, coords):
        piece = self.board[0][y][x]

        for y1 in range(y, -1, -1):
            if (y1, x) == coords: return True
            
            if self.board[0][y1][x] != '.': 
                if piece.isupper():
                    if self.board[0][y1][x] == 'k': self.bCheck = True
                    break
                else:
                    if self.board[0][y1][x] == 'K': self.wCheck = True
                    break
        for y1 in range(y, 8):
            if (y1, x) == coords: return True
            
            if self.board[0][y1][x] != '.': 
                if piece.isupper():
                    if self.board[0][y1][x] == 'k': self.bCheck = True
                    break
                else:
                    if self.board[0][y1][x] == 'K': self.wCheck = True
                    break

        for x1 in range(x, -1, -1):
            if (y1, x) == coords: return True
            
            if self.board[0][y][x1] != '.': 
                if piece.isupper():
                    if self.board[0][y][x1] == 'k': self.bCheck = True
                    break
                else:
                    if self.board[0][y][x1] == 'K': self.wCheck = True
                    break
        for x1 in range(x, 8):
            if (y1, x) == coords: return True
            
            if self.board[0][y][x1] != '.': 
                if piece.isupper():
                    if self.board[0][y][x1] == 'k': self.bCheck = True
                    break
                else:
                    if self.board[0][y][x1] == 'K': self.wCheck = True
                    break

    def checkDiagAttacks(self, x, y, coords):
        piece = self.board[0][y][x]
        
        skipBR = False
        skipBL = False
        skipTR = False
        skipTL = False

        wCheck = False
        bCheck = False

        for i in range(8):
            if (x+i, y+i) == (x,y): continue
            #BOTTOM RIGHT
            if x+i < 8 and y+i < 8 and not skipBR:
                if (y+i, x+i) == coords: return True
            
                if self.board[0][y+i][x+i] != '.':
                    if piece.isupper():
                        if self.board[0][y+i][x+i] == 'k': bCheck = True
                        skipBR = True
                    else:
                        if self.board[0][y+i][x+i] == 'K': wCheck = True
                        skipBR = True

            #BOTTOM LEFT
            if x-i >= 0 and y+i < 8 and not skipBL:
                if (y+i, x-i) == coords: return True

                if self.board[0][y+i][x-i] != '.':
                    if piece.isupper():
                        if self.board[0][y+i][x-i] == 'k': bCheck = True
                        skipBL = True
                    else:
                        if self.board[0][y+i][x-i] == 'K': wCheck = True
                        skipBL = True

            #TOP RIGHT
            if x+i < 8 and y-i < 8 and not skipTR:
                if (y-i, x+i) == coords: return True

                if self.board[0][y-i][x+i] != '.':
                    if piece.isupper():
                        if self.board[0][y-i][x+i] == 'k': bCheck = True
                        skipTR = True
                    else:
                        if self.board[0][y-i][x+i] == 'K': wCheck = True
                        skipTR = True
            #TOP LEFT
            if x-i >= 0 and y-i < 8 and not skipTL:
                print(coords, (y-i, x-i))
                if (y-i, x-i) == coords: return True

                if self.board[0][y-i][x-i] != '.':
                    if piece.isupper():
                        if self.board[0][y-i][x-i] == 'k': bCheck = True
                        skipTL = True
                    else:
                        if self.board[0][y-i][x-i] == 'K': wCheck = True
                        skipTL = True

        if bCheck: self.bCheck = True; return True
        if wCheck: self.wCheck = True; return True

    def check(self, coords=(-1,-1)):
        for y, row in enumerate(self.board[0]):
            for x, _ in enumerate(row):
                piece = self.board[0][y][x].upper()
                if piece == 'P':
                    if self.checkPawnAttacks(x, y, coords): return True
                if piece == 'R':
                    if self.checkHorAttacks(x, y, coords): return True
                if piece == 'B':
                    if self.checkDiagAttacks(x, y, coords): return True
                if piece == 'Q':
                    if self.checkDiagAttacks(x,y, coords): return True
                    if self.checkHorAttacks(x, y, coords): return True
