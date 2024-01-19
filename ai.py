import random
import copy
import logic
from pprint import pprint



class Node:
    def __init__(self, chessgame, parent = None):
        self.chessgame = chessgame
        self.parent = parent
        self.children = []

class Minimax:
    def __init__(self, current_state):
        self.current_state = Node(current_state)



    def _find_all_moves(self, node):
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
                                node.children.append(Node(temp, node))

    def _add_level(self, node):  
        if len(node.children) == 0:
            self._find_all_moves(node)
        else:
            for child in node.children:               
                self._add_level(child)
                     
    def add_level(self):
        if len(self.current_state.children) == 0:    
            self._find_all_moves(self.current_state)
        else:   
            self._add_level(self.current_state)

    def get_game_value(self):
        pass

    def _find_best_move(self, node):
        for child in node.children:
            pass
    def find_best_move(self):
        pass


class AI:

    def __init__(self, chessgame):
        self.chessgame = chessgame
        self.chessboard = self.chessgame.chessboard


    def update_chessgame(self, chessgame):
        self.chessgame = chessgame
        self.chessboard = self.chessgame.chessboard

    
    def mini_max_strategy(self):
        tree = Minimax(self.chessgame)
        tree.add_level()



    def random_strategy(self):
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

game = logic.GameLogic()
ai = AI(game)
minimax = Minimax(game)
minimax.add_level()
minimax.add_level()
minimax.add_level()

def print_board(board):
    for row in range(8):
        row_curr = []
        for col in range(8):
            row_curr.append(board[row][col].getName())
        print(row_curr)

print_board(minimax.current_state.children[0].children[0].chessgame.chessboard)
