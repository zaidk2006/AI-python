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

    def chooseBestMove(self, result):
        max = -500
        brd = copy.deepcopy(self.board)
        bestMove = None
        for moves in result:
            for move in moves:
                #brd.make_move(result[0][0], self.color)
                brd.make_move(move, self.color)
                if(self.color == 'B'):
                    score = brd.black_count - brd.white_count
                else:
                    score = brd.white_count - brd.black_count
                score = score + len(move.seq)*10
                if score > max:
                    max = score
                    bestMove = move

                brd = copy.deepcopy(self.board)

        return bestMove

        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inneir_index]
        move = self.chooseBestMove(moves)
        self.board.make_move(move ,self.color)
        return move


