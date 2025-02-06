#este ficheiro desenha o tabuleiro e as peças, e calcula os movimentos possíveis,

import pygame
from .constants import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, BEJE, BLACK, WHITE
from .piece import Piece

class Board:

    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 12
        self.create_board()

    def draw_grid(self, win):
        win.fill(BEJE)  
        for x in range (SQUARE_SIZE//2, WIDTH, SQUARE_SIZE):
            pygame.draw.line(win, BLACK, (0, x), (WIDTH, x), 4)
            pygame.draw.line(win, BLACK, (x, 0), (x, HEIGHT), 4)
        pygame.draw.line(win, BLACK, (SQUARE_SIZE//2, SQUARE_SIZE//2), (WIDTH-(SQUARE_SIZE//2), (HEIGHT-(SQUARE_SIZE//2))), 2)
        pygame.draw.line(win, BLACK, (SQUARE_SIZE//2, HEIGHT-(SQUARE_SIZE//2)), (WIDTH-(SQUARE_SIZE//2), SQUARE_SIZE//2), 2)
        pygame.draw.line(win, BLACK, (WIDTH//2, SQUARE_SIZE//2), (SQUARE_SIZE//2, HEIGHT//2), 2)
        pygame.draw.line(win, BLACK, (WIDTH//2, SQUARE_SIZE//2), (WIDTH-SQUARE_SIZE//2, HEIGHT//2), 2)
        pygame.draw.line(win, BLACK, (WIDTH//2, HEIGHT-SQUARE_SIZE//2), (SQUARE_SIZE//2, HEIGHT/2), 2)
        pygame.draw.line(win, BLACK, (WIDTH//2, HEIGHT-SQUARE_SIZE//2), (WIDTH-SQUARE_SIZE//2, HEIGHT//2), 2)

    def evaluate(self):                          #evaluation function!!
        return self.black_left-self.white_left
    
    def get_all_pieces(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece!=0 and piece.color==color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if ((row<2) or ((row==2) and (col<2))):
                    self.board[row].append(Piece(row, col, BLACK))
                elif ((row>2) or ((row==2) and (col>2))):
                    self.board[row].append(Piece(row, col, WHITE))
                else:
                    self.board[row].append(0)
    
    def draw(self, win):
        self.draw_grid(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece!=0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col]=0
            if piece!=0:
                if piece.color==WHITE:
                    self.white_left-=1
                else:
                    self.black_left-=1
    
    def winner(self):
        if self.white_left<=0:
            return BLACK
        if self.black_left<=0:
            return WHITE
        return None

    def get_valid_moves(self, piece):
        moves = {}
        col=piece.col
        left = piece.col-1
        right = piece.col+1
        row = piece.row

        if piece.color==WHITE:
            moves.update(self._horizontal(left, max(col-3, -1), -1, piece.color, row))                #ve horizontal direita
            moves.update(self._horizontal(right, min(col+3, COLS), 1, piece.color, row))              #ve horizontal esquerda
            if piece.row!=0:
                moves.update(self._vertical(row-1, max(row-3,-1), -1, piece.color, col))              #ve vertical cima
                if (piece.col==piece.row) or (piece.col==2 and piece.row==4) or (piece.col==1 and piece.row==3) or (piece.col==4 and piece.row==2) or (piece.col==3 and piece.row==1):
                    moves.update(self._traverse_left(row-1, max(row-3,-1), -1, piece.color, left))        #ve diagonal esquerda cima
                if (piece.col+1==ROWS-piece.row) or (piece.col==2 and piece.row==4) or (piece.col==3 and piece.row==3) or (piece.col==0 and piece.row==2) or (piece.col==1 and piece.row==1):
                    moves.update(self._traverse_right(row-1, max(row-3,-1), -1, piece.color, right))      #ve diagonal direita cima
                
                
        if piece.color==BLACK:
            moves.update(self._horizontal(left, max(col-3, -1), -1, piece.color, row))                #ve horizontal direita
            moves.update(self._horizontal(right, min(col+3, COLS), 1, piece.color, row))              #ve horizontal esquerda
            if piece.row!=ROWS-1:
                moves.update(self._vertical(row+1, min(row+3, ROWS), 1, piece.color, col))                #ve vertical baixo
                if (piece.col==piece.row) or (piece.col==0 and piece.row==2) or (piece.col==1 and piece.row==3) or (piece.col==2 and piece.row==0) or (piece.col==3 and piece.row==1):
                    moves.update(self._traverse_right(row+1, min(row+3,ROWS), 1, piece.color, right))         #ve diagonal direita baixo
                if (piece.col+1==ROWS-piece.row) or (piece.col==4 and piece.row==2) or (piece.col==3 and piece.row==3) or (piece.col==2 and piece.row==0) or (piece.col==1 and piece.row==1):
                    moves.update(self._traverse_left(row+1, min(row+3,ROWS), 1, piece.color, left))           #ve diagonal esquerda baixo
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left<0:
                break
            
            current = self.board[r][left]

            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step==-1:
                        row=max(r-3,-1)
                    else:
                        row=min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                    moves.update(self._vertical(r+step, row, step, color, left, skipped=last))
                break
            elif current.color==color:
                break
            else:
                last = [current]

            left-=1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right>=COLS:
                break
            
            current = self.board[r][right]

            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step==-1:
                        row=max(r-3,-1)
                    else:
                        row=min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                    moves.update(self._vertical(r+step, row, step, color, right, skipped=last)) 
                break
            elif current.color==color:
                break
            else:
                last = [current]

            right+=1

        return moves
    
    def _vertical(self, start, stop, step, color, column, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):       
            current = self.board[r][column]

            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, column)] = last + skipped
                else:
                    moves[(r, column)] = last
                
                if last:
                    if step==-1:
                        row=max(r-3,-1)
                    else:
                        row=min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, column-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, column+1, skipped=last))  
                    moves.update(self._vertical(r+step, row, step, color, column, skipped=last))     
                break
            elif current.color==color:
                break
            else:
                last = [current]
        
        return moves

    def _horizontal(self, start, stop, step, color, roww, skipped=[]):
        moves = {}
        last = []
        for c in range(start, stop, step):
            current = self.board[roww][c]

            if current==0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(roww, c)] = last + skipped
                else:
                    moves[(roww, c)] = last
                
                if last:
                    if step==-1:
                        column=max(c-3,-1)
                    else:
                        column=min(c+3, COLS)
                    moves.update(self._horizontal(c+step, column, step, color, roww, skipped=last))
                break
            elif current.color==color:
                break
            else:
                last = [current]

        return moves

