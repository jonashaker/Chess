import pieces
import copy

class CheckHandler:

    def __init__(self, chessboard):
        self.chessboard = chessboard

    def update_board(self, new_chessboard):
        self.chessboard = new_chessboard

    def get_king_position(self, color):
        """Returns current king position."""
        for row in range(8):
            for col in range(8):
                piece = self.chessboard[row][col]
                if isinstance(piece, pieces.King) and piece.color == color:
                    return (row, col)
            
    
    def is_in_check(self, color):
        """Determines if the king is in check."""
        king_pos = self.get_king_position(color)
        for row in range(8):
            for col in range(8):
                piece = self.chessboard[row][col]
                if not isinstance(piece, (pieces.EmptySquare, pieces.Pseudo_Pawn)):
                    if piece.color != color and piece.is_valid_move(self.chessboard, (row, col), king_pos):
                        return True
                
        return False
    
    def is_square_attacked(self, square, color):
        """Determines if pieces of the opposite color can move to the square."""
        temporary = self.chessboard[square[0]][square[1]]
        self.chessboard[square[0]][square[1]] = pieces.EmptySquare()

        for row in range(8):
            for col in range(8):
                attacker = self.chessboard[row][col]
                if not isinstance(attacker, (pieces.EmptySquare, pieces.Pseudo_Pawn)):
                    if attacker.color != color and attacker.is_valid_move(self.chessboard, (row, col), square):
                        self.chessboard[square[0]][square[1]] = temporary
                        return True
                    
        self.chessboard[square[0]][square[1]] = temporary

        return False

    def can_capture_or_block(self, attacker, attacker_pos, color):
        """Determines if the defending color can capture or block a pieces attacking the king."""
        # Defender tries to capture the piece.
        for row in range(8):
            for col in range(8):
                defender = self.chessboard[row][col]
                if not isinstance(attacker, (pieces.EmptySquare, pieces.Pseudo_Pawn)):
                    if defender.color == color and defender.is_valid_move(self.chessboard, (row,col), attacker_pos) and not self.is_square_attacked(attacker_pos, color):
                        return True

        # Defender tries to block the piece.
        if isinstance(attacker, (pieces.Bishop, pieces.Rook, pieces.Queen)):
            blocking_positions = self.get_blocking_positions(attacker_pos, self.get_king_position(color))
            for pos in blocking_positions:
                for row in range(8):
                    for col in range(8):
                        defender = self.chessboard[row][col]
                        if not isinstance(attacker, (pieces.EmptySquare, pieces.Pseudo_Pawn)) and not isinstance(defender, pieces.King):
                            if defender.color == color and defender.is_valid_move(self.chessboard, (row, col), pos):
                                return True 
        return False


    def get_blocking_positions(self, attacker_pos, king_pos):
        """Returns all the positions that would block the king from an attacking piece."""
        blocking_positions = []
        if attacker_pos[0] == king_pos[0]:
            for col in range(min(attacker_pos[1], king_pos[1])+1, max(attacker_pos[1], king_pos[1])):
                blocking_positions.append((attacker_pos[0], col))

        elif attacker_pos[1] == king_pos[1]:
            for row in range(min(attacker_pos[0], king_pos[0])+1, max(attacker_pos[0], king_pos[0])):
                blocking_positions.append((row, attacker_pos[1]))
        else:
            row_step = 1 if king_pos[0] > attacker_pos[0] else -1
            col_step = 1 if king_pos[1] > attacker_pos[1] else -1
            row_range = range(attacker_pos[0] + row_step, king_pos[0], row_step)
            col_range = range(attacker_pos[1] + col_step, king_pos[1], col_step)

            for row, col in zip(row_range, col_range):
                blocking_positions.append((row, col))

        return blocking_positions


    def can_escape_check(self, color):
        """Determines if the king can escape check."""
        king_pos = self.get_king_position(color)
        
        # King tries to move out of danger
        for row in range(max(0, king_pos[0]-1), min(8, king_pos[0]+2)):
            for col in range(max(0, king_pos[1]-1), min(8, king_pos[1]+2)):
                if self.chessboard[king_pos[0]][king_pos[1]].is_valid_move(self.chessboard, king_pos, (row, col)) and not self.is_square_attacked((row, col), color):
                    return True 
                
        # Pieces tries to either capture or block attacking pieces.
        for row in range(8):
            for col in range(8):
                attacker = self.chessboard[row][col]
                if not isinstance(attacker, (pieces.EmptySquare, pieces.Pseudo_Pawn)):
                    if attacker.color != color and attacker.is_valid_move(self.chessboard, (row, col), king_pos):
                        # piece is attacking king
                        if not self.can_capture_or_block(attacker, (row, col), color):
                            return False

        return True
                        
                    
    def is_checkmate(self, color):
        """Determines if a game is checkmate."""
        if self.can_escape_check(color):
            return False
        return True
        
    

                    
                    
                                
                    
                            

            


    

        




    





            



