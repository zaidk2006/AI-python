from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math
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
        self.MIN = -1000
        self.MAX = 1000

    def getBestMove(self):
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
            bestVal = -math.inf
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], False, alpha, beta)
                    bestVal = max(bestVal, val)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
            #return bestVal
        else:
            bestVal = math.inf
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], True, alpha, beta)
                    bestVal = min(bestVal, val)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
            #return bestVal
        return bestVal

    def boardScore(self, board, color):
        if(color == 1):
            return (board.black_count - board.white_count)
            #return self.smart_count(board, 1) - self.smart_count(board, 2)
        elif(color == 2):
            #return self.smart_count(board, 2) - self.smart_count(board, 1)
            return (board.white_count - board.black_count)
        else:
            return None
 
    def smart_count(self, board, color):
        result = 0.0

        color_char = ''
        if color == 1:
            color_char = 'B'
        else:
            color_char = 'W'

        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                piece_val = 5.0
                if board.board[i][j].color == color_char:
                    if board.board[i][j].is_king:
                        piece_val += 12.5
                    if i == 0 or j == 0 or i == len(board.board) - 1 or j == len(board.board[0]) - 1:
                        piece_val += 2.0

                result+=piece_val

        #print(edge, " and ", normal)
        return result

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        actions = self.board.get_all_possible_moves(self.color)
        bestScore = -math.inf
        index = randint(0, len(actions) - 1)
        innerIndex = randint(0, len(actions[index]) - 1)   
        bestMove = actions[index][innerIndex]
        for moves in actions:
            for move in moves:
                tempBoard = copy.deepcopy(self.board)
                tempBoard.make_move(move, self.color)
                #Tie with Poor AI: depth = 3, self.opponent, True
                #ok with Random: depth = 4, self.color, False
                #good with Random: depth = 3, self.opponent, False/True
                val = self.minimax(tempBoard, 3, self.opponent[self.color], True, -math.inf, math.inf)
                #print ("Value : move = %s : %s" % (val, move))
                if val > bestScore:
                    bestMove = move
                    bestScore = val

        self.board.make_move(bestMove, self.color)
        return bestMove


