import random
import copy
import logic
import checkhandler
from pprint import pprint



class _Node:
    def __init__(self, chessgame, move = None, parent = None):
        self.chessgame = chessgame
        self.move = move
        self.parent = parent
        self.children = []
        self.value = self.get_value()
        self.checkmate = False
        self.is_checkmate()

    def is_terminal(self):
        return len(self.children) == 0

    def is_checkmate(self):
        check_handler = checkhandler.CheckHandler(self.chessgame.chessboard)
        if check_handler.is_in_check(self.chessgame.turn):
            if check_handler.is_checkmate(self.chessgame.turn):
                self.checkmate = True
                if self.chessgame.turn == "white":
                    self.value = float('inf')
                else:
                    self.value = float('-inf')


    def get_value(self):
        value = 0
        for row in range(8):
            for col in range(8):
                piece = self.chessgame.chessboard[row][col]
                if not piece.color is None:
                    if piece.color == "black":
                        value += piece.get_value() 
                    else:
                        value -= piece.get_value()
        return value
    
class Minimax:
    def __init__(self, chessgame):
        self.chessgame = _Node(chessgame)
        self.depth = 0
        self.add_level()
        self.add_level()
      
        self.times_used = 0

    def _find_all_moves(self, node):
        if node.checkmate is True:
            return
        chess_state = node.chessgame
        for row in range(8):
            for col in range(8):
                piece = chess_state.chessboard[row][col]
                if piece.color == chess_state.turn:
                    for r in range(8):
                        for c in range(8):
                            if chess_state.is_valid_move((row, col), (r, c)):
                                temp = copy.deepcopy(chess_state)
                                temp.make_move((row, col), (r, c))
                                node.children.append(_Node(temp, ((row, col), (r, c)), node))

    def _add_level(self, node):  
        if len(node.children) == 0:
            self._find_all_moves(node)
        else:
            for child in node.children:               
                self._add_level(child)
                     
    def add_level(self):
        if len(self.chessgame.children) == 0:    
            self._find_all_moves(self.chessgame)
        else:   
            self._add_level(self.chessgame)
        self.depth += 1

    def minimax(self, depth, node, alpha, beta, maximizingPlayer):
        if depth == 0 or node.is_terminal():
            self.times_used += 1
            return node.get_value()
        
        if maximizingPlayer:
            maxEval = float('-inf')
            for child in node.children:
                eval = self.minimax(depth - 1, child, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            for child in node.children:
                eval = self.minimax(depth - 1, child, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def choose_best_move(self):
        best_move = None
        best_value = float('-inf')
        for child in self.chessgame.children:
            value = self.minimax(self.depth - 1, child, float('-inf'), float('inf'), False)
            if value > best_value:
                best_value = value
                best_move = child.move  

        print(self.times_used)
        return best_move


class RandomStrategy:
    def __init__(self, chessgame):
        self.chessgame = chessgame 

    def find_move(self):
        possible_moves = []
        wgt = []
        for row in range(8):
            for col in range(8):
                piece = self.chessboard[row][col]
                if piece.color == self.chessgame.turn:
                    curr_moves = self.get_valid_moves((row, col))
                    if len(curr_moves) != 0:
                        possible_moves.append(((row, col), random.choice(curr_moves)))
                        wgt.append(len(curr_moves))
 
        decision = random.choices(possible_moves, wgt)[0]
       
        return decision[0], decision[1]
    
    def get_valid_moves(self, pos):
        piece = self.chessboard[pos[0]][pos[1]]
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if piece.is_valid_move(self.chessboard, pos, (row, col)):
                    temp = copy.deepcopy(self.chessgame)
                    temp.update_board(pos, (row, col))
                    if not temp.check_handler.is_in_check(self.chessgame.turn):
                        valid_moves.append((row, col))
        return valid_moves


    



