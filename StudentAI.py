from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

movePairs = {}
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
        self.MIN = -1000
        self.MAX = 1000
        #self.movePairs = {}

    def getBestMove(self):
        #print("for player: ", self.color)
        #print("move pairs: ", self.movePairs)
        global movePairs
        v = list(movePairs.values())
        k = list(movePairs.keys())
        bestMove = k[v.index(max(v))]
        return bestMove
            	
    # new alpha beta recursive function
    def minimax(self, board, depth, color, isMaxPlayer, alpha, beta):
        #global movePairs
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
                    val = self.minimax(board, depth-1, self.opponent[color], False, alpha, beta)
                    #movePairs.update( {val : move} )
                    #print("INSIDE MAX: ", movePairs)
                    bestVal = max(bestVal, val)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        return bestVal
            return bestVal
        else:
            bestVal = self.MAX
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(board, depth-1, self.opponent[color], True, alpha, beta)
                    bestVal = min(bestVal, val)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        return bestVal
            return bestVal
            

    def boardScore(self, board, color):
        if(color == 1):
            return board.black_count - board.white_count
        elif(color == 2):
            return board.white_count - board.black_count
        else:
            return None
        
    def get_move(self,move):
        global movePairs
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        actions = self.board.get_all_possible_moves(self.color)
        #tempMoves = copy.deepcopy(actions)
        bestScore = -1000
        index = randint(0, len(actions) - 1)
        #index = 0
        innerIndex = randint(0, len(actions[index]) - 1)   
        #innerIndex = randint(0, len([for moves in tempMoves]) - 1)
        bestMove = actions[index][innerIndex]
        for moves in actions:
            for move in moves:
                tempBoard = copy.deepcopy(self.board)
                tempBoard.make_move(move, self.color)
                val = self.minimax(tempBoard, 3, self.color, True, self.MIN, self.MAX)
                if val > bestScore:
                    bestMove = move
                    bestScore = val
        #my comment
        """
        v = list(movePairs.values())
        k = list(movePairs.keys())
        bestMove = k[v.index(max(v))]
        movePairs.clear()
        """
        self.board.make_move(bestMove, self.color)
        return bestMove


