from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math
import random
from timeit import default_timer as timer
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
        self.MIN = -1000
        self.MAX = 1000

    # new alpha beta recursive function
    def minimax(self, board, depth, color, isMaxPlayer, alpha, beta):
        if depth == 0:
            return self.boardScore(board, color)

        actions = board.get_all_possible_moves(color)
        if isMaxPlayer:
            bestVal = float('-inf')
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], not isMaxPlayer, alpha, beta)
                    bestVal = max(bestVal, val)
                    alpha = max(alpha, bestVal)
                    if beta <= alpha:
                        break
        else:
            bestVal = float('inf')
            for moves in actions:
                for move in moves:
                    tempBoard = copy.deepcopy(board)
                    tempBoard.make_move(move, color)
                    val = self.minimax(tempBoard, depth-1, self.opponent[color], not isMaxPlayer, alpha, beta)
                    bestVal = min(bestVal, val)
                    beta = min(beta, bestVal)
                    if beta <= alpha:
                        break
        return bestVal

      
    def isCheckerEdge(self, i, j, boardRow, boardColumn):
        return (i == 0 or i == boardRow - 1 or j == 0 or j == boardColumn - 1) # i=0, j=0 checks top left hand : boardRow-1, boardColumn-1 checks bot right _|

    def isHalfway(self, i, board, color):
        midBoard = len(board.board)/2
        if len(board.board) % 2 == 0: # rows is even
            return (color == 'B' and (i == midBoard or i == midBoard+1)) or (color == 'W' and (i == midBoard-1 or i == midBoard-2))
        else:
            return (color == 'B' and (i == math.floor(midBoard)+1 or i == math.floor(midBoard))) or (color == 'W' and (i == math.floor(midBoard) or i == math.floor(midBoard)-1)) 
                
    def isAdvPawn(self, i, board, color):
        midBoard = len(board.board)/2
        if len(board.board) % 2 == 0:
            return (color == 'B' and (i >= midBoard)) or (color == 'W' and (i < midBoard))
        else:
            return (color == 'B' and (i >= math.ceil(midBoard))) or (color == 'W' and (i < math.floor(midBoard)))

    # score weighted by: # kings, checker evaluation 
    # used to evaluate kings for both us and then opponent
    def checkerEval(self, board, color):
        kingCnt = 0
        oppKingCnt = 0
        checkerScore = 0
        oppCheckerScore = 0
        checkerColor = ''

        if color == 1:
            checkerColor = 'B'
        else:
            checkerColor = 'W'
        # iterate through each spot on board
        for i in range(len(board.board)): # rows
            for j in range(len(board.board[i])): # columns
                if board.board[i][j].is_king: # piece is a king
                    if board.board[i][j].color == checkerColor: # our king
                        kingCnt += 1
                        if self.isHalfway(i, board, checkerColor): # if our king halfway
                            checkerScore += 5
                    else: # opponent's king
                        oppKingCnt += 1
                        if self.isHalfway(i, board, board.board[i][j].color): # if opponent king halfway
                            oppCheckerScore += 5

                else: # piece is a pawn
                    if board.board[i][j].color == checkerColor: # evaluate advance pawn for ours
                        if self.isAdvPawn(i, board, checkerColor):
                            checkerScore += 3
                    else: # evaluate advance pawn for opponent 
                        if self.isAdvPawn(i, board, board.board[i][j].color):
                            oppCheckerScore += 3 
                  
                if self.isCheckerEdge(i, j, len(board.board), len(board.board[0])): # piece is an edge piece
                    checkerScore += 1
                    """
                    if board.board[i][i].color == checkerColor: # our edge piece
                        checkerScore += 1
                    else: # opponent's edge piece
                        oppCheckerScore += 1
                    """
        return ((10*kingCnt + checkerScore) - (10*oppKingCnt + oppCheckerScore))

                  
    def checkersDiff(self, board, color):
        if(color == 1):
            return board.black_count - board.white_count
        else:
            return board.white_count - board.black_count

    # calculate score of board
    def boardScore(self, board, color):
        score = 0
        # 5 weight
        score += 5 * self.checkersDiff(board, color)
        score += self.checkerEval(board, color) 
        return score
   
    # choose best move
    def boardBestMove(self):
        moveScore = {}
        actions = self.board.get_all_possible_moves(self.color)
        bestScore = float('-inf')
        index = randint(0, len(actions) - 1)
        innerIndex = randint(0, len(actions[index]) - 1)   
        bestMove = actions[index][innerIndex]
        for moves in actions:
            for move in moves:
                tempBoard = copy.deepcopy(self.board)
                tempBoard.make_move(move, self.color)
                val = self.minimax(tempBoard, 3, self.opponent[self.color], False, -math.inf, math.inf) 
                # store move and val 
                moveScore[move] = val

        #adds random factor
        v = list(moveScore.values()) # make list of values
        allBestMoves = []
        maxValue = max(v)
        for move, score in moveScore.items(): # .items() turns dictionary into list
            if score == maxValue:
                allBestMoves.append(move) # find all moves with same max score
        bestMove = random.choice(allBestMoves)        
        return bestMove
 

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        bestMove = self.boardBestMove()
        self.board.make_move(bestMove, self.color)
        return bestMove


