class logic:
    def __init__(self, mainLogic):
        self.mainLogic = mainLogic

    def colorHor(self, list, x, y):
        board = self.mainLogic.board
        
        stop = False
        for i in range(y-1, -1, -1):
            if stop: break

            if board[0][i][x] != '.': 
                if board[0][y][x].isupper() != board[0][i][x].isupper():
                    stop = True
                else:
                    break

            list[i*8+x][0]['bg']='green'

        stop=False
        for i in range(y+1, 8):
            if stop: break

            if board[0][i][x] != '.': 
                if board[0][y][x].isupper() != board[0][i][x].isupper():
                    stop = True
                else:
                    break

            list[i*8+x][0]['bg']='green'

        stop=False
        for i in range(x-1, -1, -1):
            if stop: break

            if board[0][y][i] != '.': 
                if board[0][y][x].isupper() != board[0][y][i].isupper():
                    stop = True
                else:
                    break

            list[y*8+i][0]['bg']='green'

        stop=False
        for i in range(x+1, 8):
            print(i)
            if stop: break

            if board[0][y][i] != '.': 
                if board[0][y][x].isupper() != board[0][y][i].isupper():
                    stop = True
                else:
                    break

            list[y*8+i][0]['bg']='green'

    def colorPawn(self, list, x, y):
        board = self.mainLogic.board

        if self.mainLogic.turn:
            if board[0][y-1][x] == '.':
                list[(y-1)*8+x][0]['bg']='green'

            if y == 6:
                if board[0][y-2][x] and board[0][y-1][x] == '.':
                    list[4*8+x][0]['bg']='green'

            try:
                left = board[0][y-1][x-1]
                if left != '.':
                    if left.isupper() != board[0][y][x].isupper():
                        list[(y-1)*8+x-1][0]['bg']='green'
            except Exception: pass

            try:
                right = board[0][y-1][x+1]
                if right != '.':
                    if right.isupper() != board[0][y][x].isupper():
                        list[(y-1)*8+x+1][0]['bg']='green'
            except Exception: pass

            if (x-1, y-1) == self.mainLogic.enPassentSquare:
                list[(y-1)*8+x-1][0]['bg']='green'
            if (x+1, y-1) == self.mainLogic.enPassentSquare:
                list[(y-1)*8+x+1][0]['bg']='green'

        else:
            if board[0][y+1][x] == '.':
                list[(y+1)*8+x][0]['bg']='green'

            if y == 1:
                if board[0][y+2][x] and board[0][y+1][x] == '.':
                    list[3*8+x][0]['bg']='green'

            try:
                left = board[0][y+1][x-1]
                if left != '.':
                    if left.isupper() != board[0][y][x].isupper():
                        list[(y+1)*8+x-1][0]['bg']='green'
            except Exception: pass
            
            try:
                right = board[0][y+1][x+1]
                if right != '.':
                    if right.isupper() != board[0][y][x].isupper():
                        list[(y+1)*8+x+1][0]['bg']='green'
            except Exception: pass

            if (x-1, y+1) == self.mainLogic.enPassentSquare:
                list[(y+1)*8+x-1][0]['bg']='green'
            if (x+1, y+1) == self.mainLogic.enPassentSquare:
                list[(y+1)*8+x+1][0]['bg']='green'

    def colorDiag(self, list, x, y):
        board = self.mainLogic.board

        stop = False
        for i in range(1, 8-y):
            
            if stop:
                stop = False
                break

            if y+i > 7: break
            if x+i > 7: break

            if board[0][y+i][x+i] != '.':
                if board[0][y+i][x+i].isupper() != board[0][y][x].isupper(): stop = True
                else: break

            list[(y+i)*8+x+i][0]['bg']='green'
        for i in range(1, 8-y):
            
            if stop:
                stop = False
                break

            if y+i > 7: break
            if x-i < 0: break

            if board[0][y+i][x-i] != '.':
                if board[0][y+i][x-i].isupper() != board[0][y][x].isupper(): stop = True
                else: break
                
            list[(y+i)*8+x-i][0]['bg']='green'

        for i in range(1, y):
            
            if stop:
                stop = False
                break

            if y-i < 0: break
            if x+i > 7: break

            if board[0][y-i][x+i] != '.':
                if board[0][y-i][x+i].isupper() != board[0][y][x].isupper(): stop = True
                else: break

            list[(y-i)*8+x+i][0]['bg']='green'
        for i in range(1, y):
            if stop:
                stop = False
                break

            if y-i < 0: break
            if x-i < 0: break

            if board[0][y-i][x-i] != '.':
                if board[0][y-i][x-i].isupper() != board[0][y][x].isupper(): stop = True
                else: break
                
            list[(y-i)*8+x-i][0]['bg']='green'

    def colorKnight(self, list, x, y):
        board = self.mainLogic.board

        squares = [(y-2, x-1), (y-2, x+1), (y-1, x+2), (y-1, x-2), (y+1, x+2), (y+1, x-2), (y+2, x+1), (y+2, x-1)]

        stop = False
        for i in squares:
            try:
                y1 = i[0]
                x1 = i[1]
            
                if 0>x1 or x1>8: continue
                if 0>y1 or y1>8: continue

                if board[0][y1][x1] != '.':
                    if board[0][y1][x1].isupper() == board[0][y][x].isupper(): continue

                list[y1*8+x1][0]['bg']='green'

            except Exception: pass

    def colorKing(self, list, x, y):
        board = self.mainLogic.board
        piece = board[0][y][x]

        for y1 in [y-1, y, y+1]:
            for x1 in [x-1, x, x+1]:
                if 0>x1 or x1>7: continue
                if 0>y1 or y1>7: continue

                if board[0][y1][x1] != '.' and board[0][y1][x1].isupper() == piece.isupper(): continue

                list[y1*8+x1][0]['bg']='green'
        print(y)
        if self.mainLogic.turn:
            if (y, x) == self.mainLogic.wKingStart:
                if self.mainLogic.wOO:
                    if board[0][y][x+1] == '.' and board[0][y][x+2] == '.' and board[0][y][x+3]=='R':
                        list[y*8+x+2][0]['bg']='green'
                if self.mainLogic.wOOO:
                    if board[0][y][x-1] == '.' and board[0][y][x-2]=='.' and board[0][y][x-3]=='.'and board[0][y][x-4]=='R':
                        list[y*8+x-2][0]['bg']='green'

    def colorAvailableSquares(self, list, ix):
        piece = list[ix][1].upper()
        if piece == 'R':
            self.colorHor(list, list[ix][2], list[ix][3])
        if piece == 'P':
            self.colorPawn(list, list[ix][2], list[ix][3])
        if piece == 'B':
            self.colorDiag(list, list[ix][2], list[ix][3])
        if piece == 'N':
            self.colorKnight(list, list[ix][2], list[ix][3])
        if piece == 'Q':
            self.colorHor(list, list[ix][2], list[ix][3])
            self.colorDiag(list, list[ix][2], list[ix][3])
        if piece == 'K':
            self.colorKing(list, list[ix][2], list[ix][3])