from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math
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
        return (i == 0 or i == boardRow - 1 or j == 0 or j == boardColumn - 1)


    def checkerEval(self, board, color):
        kingCnt = 0
        checkerScore = 0
        checkerColor = ''

        if color == 1:
            checkerColor = 'B'
        else:
            checkerColor = 'W'

        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                if board.board[i][j].color == checkerColor and board.board[i][j].is_king:
                    kingCnt += 1
                if self.isCheckerEdge(i, j, len(board.board), len(board.board[0])):
                    checkerScore += 1

        return (10 * kingCnt) + checkerScore

    
    def checkersDiff(self, board, color):
        if(color == 1):
            return board.black_count - board.white_count
        else:
            return board.white_count - board.black_count


    def boardScore(self, board, color):
        score = 0
        score += 5 * self.checkersDiff(board, color)
        score += self.checkerEval(board, color) - self.checkerEval(board, self.opponent[color])
        return score
   
    
    def boardBestMove(self):
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
                if val > bestScore:
                    bestMove = move
                    bestScore = val

        return bestMove
 

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        bestMove = self.boardBestMove()
        self.board.make_move(bestMove, self.color)
        return bestMove


