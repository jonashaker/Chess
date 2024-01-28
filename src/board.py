import pieces
import copy
from checkhandler import CheckHandler

class ChessGame:

    def __init__(self):
        self.chessboard = [[pieces.Rook("white"), pieces.Knight("white"), pieces.Bishop("white"), pieces.Queen("white"), pieces.King("white"), pieces.Bishop("white"), pieces.Knight("white"), pieces.Rook("white")],
                    [pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white"), pieces.Pawn("white")],
                    [pieces.EmptySquare()]*8,
                    [pieces.EmptySquare()]*8,
                    [pieces.EmptySquare()]*8,
                    [pieces.EmptySquare()]*8,
                    [pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black"), pieces.Pawn("black")],
                    [pieces.Rook("black"), pieces.Knight("black"), pieces.Bishop("black"), pieces.Queen("black"), pieces.King("black"), pieces.Bishop("black"), pieces.Knight("black"), pieces.Rook("black")]]

        self.turn = "white"

        self.check_mate = False
        self.check = False

        self.check_handler = CheckHandler(self.chessboard)

    
    def castling(self, start, to):
        """Implements the castling maneuver."""
        if isinstance(self.chessboard[start[0]][start[1]], pieces.Rook):
            placeholder = start 
            start = to 
            to = placeholder

        if abs(start[1]-to[1]) == 3:
            # Short castling
            self.chessboard[to[0]][to[1]-1] = self.chessboard[start[0]][start[1]]
            self.chessboard[to[0]][to[1]-2] = pieces.Rook("%s" % self.chessboard[start[0]][start[1]].color)
            self.chessboard[to[0]][to[1]-1].moved = True

        else:
            # Long castling
            self.chessboard[to[0]][to[1]+2] = self.chessboard[start[0]][start[1]]
            self.chessboard[to[0]][to[1]+3] = pieces.Rook("%s" % self.chessboard[start[0]][start[1]].color)
            self.chessboard[to[0]][to[1]+2].moved = True


        self.chessboard[start[0]][start[1]] = pieces.EmptySquare()
        self.chessboard[to[0]][to[1]] = pieces.EmptySquare()
        
    def en_passant(self, start, to):
        """Implements the en passant maneuver."""
        if self.chessboard[start[0]][start[1]].is_white():
            self.chessboard[to[0]-1][to[1]] = pieces.EmptySquare()
        else:
            self.chessboard[to[0]+1][to[1]] = pieces.EmptySquare()
        
        
    def create_pseudo_pawn(self, start):
        """Creates a pseudo pawn that takes care of the en passant rule."""
        if self.chessboard[start[0]][start[1]].is_white():
            self.chessboard[start[0]+1][start[1]] = pieces.Pseudo_Pawn()
        else:
            self.chessboard[start[0]-1][start[1]] = pieces.Pseudo_Pawn()

    def promotion(self, start, to):
        """Implements the pawn promotion rule."""
        self.chessboard[to[0]][to[1]] = pieces.Queen("%s" % self.chessboard[start[0]][start[1]].color)
        self.chessboard[start[0]][start[1]] = pieces.EmptySquare()
       
    
    def switch_turn(self):
        """Switches the turn attribute."""
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
    
    def check_turn(self, pos):
        """Returns True if the piece on a certain position is the turn color."""
        piece = self.chessboard[pos[0]][pos[1]]
        return piece.color == self.turn
    
    def is_in_check(self):
        """Checks if the player is in check."""
        if self.check_handler.is_in_check(self.turn):
            return True
        return False
    
    def is_checkmate(self):
        """Checks if the player is check mate."""
        if self.check_handler.is_checkmate(self.turn):
            return True 
        else:
            return False


    def clear_pseudo_pawns(self):
        for col in range(8):
            # Clear all pseudo-pawns from the board to hinder pawns from making a faulty en passant kill.
            if isinstance(self.chessboard[2][col], pieces.Pseudo_Pawn):
                self.chessboard[2][col] = pieces.EmptySquare()

            if isinstance(self.chessboard[5][col], pieces.Pseudo_Pawn):
                self.chessboard[5][col] = pieces.EmptySquare() 

    def update_board(self, start, to):

        """Implements regular moves and the three special rules: Castling, pawn promotion and en passant."""
        if abs(to[0]-3.5) == 3.5 and isinstance(self.chessboard[start[0]][start[1]], pieces.Pawn):
            # Promote pawn
            self.promotion(start, to)
            return
        
        if (isinstance(self.chessboard[start[0]][start[1]], pieces.King) and isinstance(self.chessboard[to[0]][to[1]], pieces.Rook)) or (isinstance(self.chessboard[start[0]][start[1]], pieces.Rook) and isinstance(self.chessboard[to[0]][to[1]], pieces.King)):
            
            # Castling
            self.castling(start, to)
    
        if isinstance(self.chessboard[start[0]][start[1]], pieces.Pawn) and isinstance(self.chessboard[to[0]][to[1]], pieces.Pseudo_Pawn):
            # En passant
            self.en_passant(start, to)
        
        self.clear_pseudo_pawns()

        if isinstance(self.chessboard[start[0]][start[1]], pieces.Pawn) and abs(to[0]-start[0]) == 2:
            # Create pseudo pawn behind a double jumping pawn.
            self.create_pseudo_pawn(start)

        if isinstance(self.chessboard[start[0]][start[1]], pieces.King) or isinstance(self.chessboard[start[0]][start[1]], pieces.Rook):
            # Trigger the moved attribute whenever the king or rook moves.
            self.chessboard[start[0]][start[1]].moved = True
            
        self.chessboard[to[0]][to[1]] = self.chessboard[start[0]][start[1]]
        self.chessboard[start[0]][start[1]] = pieces.EmptySquare()
        
        # Update checkhandler infor about the board
        self.check_handler.update_board(self.chessboard)

    def make_move(self, start, to):
        self.update_board(start, to)
        self.switch_turn()

    def is_valid_move(self, start, to):
        """Determines if a given move is valid wrt to initial position, target position and turn."""
        piece = self.chessboard[start[0]][start[1]]
        if piece.color != self.turn:
            return False
        
        if self.chessboard[start[0]][start[1]].is_valid_move(self.chessboard, start, to):
            temp = copy.deepcopy(self.chessboard)
            self.update_board(start, to)
            if self.check_handler.is_in_check(self.turn):
                # Checks if the move puts the player's own king in check.
                self.chessboard = temp 
                self.check_handler.chessboard = self.chessboard
                return False
            else:
                self.chessboard = temp 
                self.check_handler.chessboard = self.chessboard
                return True 
        return False