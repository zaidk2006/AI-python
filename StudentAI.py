from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.d = 3
        self.bestMove = None

    def alphaBetaMinMax(self, board):
        v = self.max_value(board, -10000, 10000, 0)
        """actions = board.get_all_possible_moves(self.color)
        for moves in actions:
            for move in moves:
                tmpBrd = copy.deepcopy(board)
                tmpBrd.make_move(move, self.color)
                score = self.boardScore(tmpBrd)
                if score == v:
                    return move
        return actions[0][0] 
        """
        return self.bestMove

    def max_value(self, board, alpha, beta, depth):
        actions = board.get_all_possible_moves(self.color)
        if(depth >= self.d or len(actions) == 0):
            return self.boardScore(board)
        v = -10000
        for moves in actions:
            for move in moves:
                tmpBrd = copy.deepcopy(board)
                tmpBrd.make_move(move, self.color)
                v = max(v, self.min_value(tmpBrd, alpha, beta, depth+1))
                self.bestMove = move
                if v >= beta:
                    return v;
                alpha = max(alpha, v)
        return v


    def min_value(self, board, alpha, beta, depth):
        actions = board.get_all_possible_moves(self.opponent[self.color])
        if(depth >= self.d or len(actions) == 0):
            return self.boardScore(board)
        v = 10000
        for moves in actions:
            for move in moves:
                tmpBrd = copy.deepcopy(board)
                tmpBrd.make_move(move, self.opponent[self.color])
                v = min(v, self.max_value(tmpBrd, alpha, beta, depth+1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
       
        return v


    def boardScore(self, board):
        if(self.color == 1):
            return board.black_count - board.white_count
        elif(self.color == 2):
            return board.white_count - board.black_count
        else:
            return None
        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inneir_index]
        move = self.alphaBetaMinMax(self.board)
        self.board.make_move(move ,self.color)
        return move


