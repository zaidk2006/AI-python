from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():
    movePairs = {}

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
        self.MIN = -1000
        self.MAX = 1000
        #self.movePairs = {}

    def getBestMove(self):
        print("for player: ", self.color)
        print("move pairs: ", self.movePairs)
        bestVal = max(self.movePairs.keys())
        return self.movePairs.get(bestVal)
            	

    def minimax(self, board, depth, color, isMaxPlayer, alpha, beta):
        actions = board.get_all_possible_moves(color)
        if depth == 0 or len(actions) == 0:
            return self.boardScore(board, color)
        if isMaxPlayer:
            #max player is both in self mode since both are using this algorithm
            #if you print here, it will print for both players as if you are black/white
            bestVal = self.MIN
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], False, alpha, beta)
                    global movePairs
                    movePairs.update( {val : move} )
                    print("INSIDE MAX: ", self.movePairs)
                    bestVal = max(bestVal, val)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
            return bestVal
        else:
            bestVal = self.MAX
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], True, alpha, beta)
                    bestVal = min(bestVal, val)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
            return bestVal
            

    def boardScore(self, board, color):
        if(color == 1):
            return board.black_count - board.white_count
        elif(color == 2):
            return board.white_count - board.black_count
        else:
            return None
        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        self.minimax(self.board, 3, self.color, True, self.MIN, self.MAX)
        move = self.getBestMove()
        self.board.make_move(move, self.color)
        return move


