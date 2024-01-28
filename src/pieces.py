import checkhandler

class Piece(object):
    """Base class for a chess square."""

    def __init__(self):
        pass

    def getName(self):
        """Returns name of the piece that inhabits the square."""
        return self.__class__.__name__

    def is_white(self):
        """Checks if the square is white."""
        return self.color == "white"

    def is_black(self):
        """Checks if the square is black."""
        return self.color == "black"

    def is_empty(self):
        """Checks if the square is empty."""
        return self.color is None

class EmptySquare(Piece):
    def __init__(self):
        """Represents and empty square on the chessboard."""
        super().__init__()
        self.color = None
        
class Pawn(Piece):
    def __init__(self, color):
        """Represents a pawn piece on the chessboard."""
        super().__init__()
        self.color = color

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        if Piece.is_white(self):
            if abs(start[1]-to[1]) == 1:
                # White tries to defeat an enemy with a pawn
                if to[0]-start[0] == 1:
                    return Piece.is_black(target_square) or isinstance(target_square, Pseudo_Pawn)
                else:
                    return False
            elif to[1] == start[1]:
                # White tries to advance straight with pawn
                if to[0]-start[0] == 1:
                    return Piece.is_empty(target_square)
                elif start[0] == 1 and to[0]-start[0] == 2:
                    return Piece.is_empty(target_square) and Piece.is_empty(chessboard[to[0]-1][to[1]])
                else:
                    return False
            else:
                return False
        else:
            if abs(start[1]-to[1]) == 1:
                # Black tries to defeat an enemy with a pawn
                if to[0]-start[0] == -1:
                    return Piece.is_white(target_square) or isinstance(target_square, Pseudo_Pawn)
                else:
                    return False
            elif to[1] == start[1]:
                # Black tries to advance straight with pawn
                if to[0]-start[0] == -1:
                    return Piece.is_empty(target_square)
                elif start[0] == 6 and to[0]-start[0] == -2:
                    return (Piece.is_empty(target_square) and Piece.is_empty(chessboard[to[0]+1][to[1]]))
                else:
                    return False
            else:
                return False
    
    def get_value(self):
        return 1


class Pseudo_Pawn(Piece):

    def __init__(self):
        """Represents a pseudo-pawn piece on the chessboard which is required to implement en-passant."""
        super().__init__()
        self.color = None

    def get_value(self):
        return 0

class Rook(Piece):

    def __init__(self, color):
        """Represents a rook piece on the chessboard."""
        super().__init__()
        self.color = color
        self.moved = False

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        if start[0] == to[0]:
            # Rook moves sideways
            if isinstance(target_square, King) and target_square.color == chessboard[start[0]][start[1]].color:
                return chessboard[to[0]][to[1]].is_valid_move(chessboard, to, start)
            if abs(to[1]-start[1]) >= 2:
                # EmptySquare spaces between initial position and goal
                for i in range(min(start[1], to[1])+1,max(start[1], to[1])):
                    if not Piece.is_empty(chessboard[to[0]][i]):
                        return False

            if Piece.is_white(self):
                if not Piece.is_white(target_square):
                    return True
            else:
                if not Piece.is_black(target_square):
                    return True

        elif start[1] == to[1]:
            # Rook moves forward/backwards
            if abs(to[0]-start[0]) >= 2:
                # EmptySquare spaces between initial position and goal
                for i in range(min(start[0], to[0])+1, max(start[0], to[0])):
                    if not Piece.is_empty(chessboard[i][to[1]]):
                        return False

            if Piece.is_white(self):
                if not Piece.is_white(target_square):
                    return True
            else:
                if not Piece.is_black(target_square):
                    return True
                
        else:
            return False

    def get_value(self):
        return 5
    
class Bishop(Piece):

    def __init__(self, color):
        """Represents a bishop piece on the chessboard."""
        super().__init__()
        self.color = color

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        if abs(to[0]-start[0]) == abs(to[1]-start[1]):
            # Legal move
            if abs(to[1]-start[1]) >= 2:
                # EmptySquare positions between start and goal. Four cases:
                if to[0] > start[0] and to[1] > start[1]:
                    # Move down right
                    for i in range(1, abs(to[1]-start[1])):
                        if not Piece.is_empty(chessboard[start[0] + i][start[1] + i]):
                            return False
                elif to[0] > start[0] and to[1] < start[1]:
                    # Move down left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] + i][start[1] - i]):
                            return False
                elif to[0] < start[0] and to[1] > start[1]:
                    # Move up right
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] - i][start[1] + i]):
                            return False
                else:
                    # Move up left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] - i][start[1] - i]):
                            return False

            if Piece.is_white(self):
                return not Piece.is_white(target_square)
            else:
                return not Piece.is_black(target_square)
        else:
            return False

    def get_value(self):
        return 3

class Knight(Piece):

    def __init__(self, color):
        """Represents a knight piece on the chessboard."""
        super().__init__()
        self.color = color

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        if abs(to[0]-start[0]) == 2 and abs(to[1]-start[1]) == 1 or abs(to[0]-start[0]) == 1 and abs(to[1]-start[1]) == 2:
            if Piece.is_white(self):
                return not Piece.is_white(target_square)
            else:
                return not Piece.is_black(target_square)
        else:
            return False
    
    def get_value(self):
        return 3

class Queen(Piece):

    def __init__(self, color):
        """Represents a Queen piece on the chessboard."""
        super().__init__()
        self.color = color

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        if start[0] == to[0] or start[1] == to[1]:
            # Move as rook
            if start[0] == to[0]:
                # Rook moves sideways
                if abs(to[1]-start[1]) >= 2:
                    # EmptySquare spaces between initial position and goal
                    for i in range(min(start[1], to[1])+1,max(start[1], to[1])):
                        if not Piece.is_empty(chessboard[to[0]][i]):
                            return False

                if Piece.is_white(self):
                    return not Piece.is_white(target_square)
                else:
                    return not Piece.is_black(target_square)

            elif start[1] == to[1]:
                # Rook moves forward/backwards
                if abs(to[0]-start[0]) >= 2:
                    # EmptySquare spaces between initial position and goal
                    for i in range(min(start[0], to[0])+1,max(start[0], to[0])):
                        if not Piece.is_empty(chessboard[i][to[1]]):
                            return False

                if Piece.is_white(self):
                    return not Piece.is_white(target_square)
                else:
                    return not Piece.is_black(target_square)
            else:
                return False
                
        elif abs(to[0]-start[0]) == abs(to[1]-start[1]):
            # Move as Bishop
            if abs(to[1]-start[1]) >= 2:
                # EmptySquare positions between start and goal. Four cases:
                if to[0] > start[0] and to[1] > start[1]:
                    # Move down right
                    for i in range(1, abs(to[1]-start[1])):
                        if not Piece.is_empty(chessboard[start[0] + i][start[1] + i]):
                            return False
                elif to[0] > start[0] and to[1] < start[1]:
                    # Move down left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] + i][start[1] - i]):
                            return False
                elif to[0] < start[0] and to[1] > start[1]:
                    # Move up right
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] - i][start[1] + i]):
                            return False
                else:
                    # Move up left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(chessboard[start[0] - i][start[1] - i]):
                            return False
                        
            if Piece.is_white(self):
                return not Piece.is_white(target_square)
            else:
                return not Piece.is_black(target_square)
        else:
            return False

    def get_value(self):
        return 9
    
class King(Piece):

    def __init__(self, color):
        """Represents a king piece on the chessboard."""
        super().__init__()
        self.color = color
        self.moved = False

    def is_valid_move(self, chessboard, start, to):
        """Checks if a certain move is valid."""
        target_square = chessboard[to[0]][to[1]]
        check_handler = checkhandler.CheckHandler(chessboard)

        if abs(start[0]-to[0]) <= 1 and abs(start[1]-to[1]) <= 1:
            if Piece.is_white(self):
                if not Piece.is_white(target_square):
                    return True
            else:
                if not Piece.is_black(target_square):
                    return True
            return False
            
        elif self.moved == False and Piece.is_white(self) and isinstance(target_square, Rook):
            # White tries to castle
            if target_square == chessboard[0][0]:
                # Long castling
                if Piece.is_empty(chessboard[0][1]) and Piece.is_empty(chessboard[0][2]) and Piece.is_empty(chessboard[0][3]) and target_square.moved is False:
                    if not (check_handler.is_square_attacked((0,1), target_square.color) or check_handler.is_square_attacked((0,2), target_square.color) or check_handler.is_square_attacked((0,3), target_square.color)):
                        return True
                
            elif target_square == chessboard[0][7]:
                # Short castling
                if Piece.is_empty(chessboard[0][5]) and Piece.is_empty(chessboard[0][6]) and target_square.moved is False:
                    if not (check_handler.is_square_attacked((0,5), target_square.color) or check_handler.is_square_attacked((0,6), target_square.color)):
                        return True
                
            return False
        
        elif self.moved == False and Piece.is_black(self) and isinstance(target_square, Rook):
            # Black tries to castle
            if target_square == chessboard[7][0]:
                # Long castling
                if Piece.is_empty(chessboard[7][1]) and Piece.is_empty(chessboard[7][2]) and Piece.is_empty(chessboard[7][3]) and target_square.moved is False:
                    if not (check_handler.is_square_attacked((7,1), target_square.color) or check_handler.is_square_attacked((7,2), target_square.color) or check_handler.is_square_attacked((7,3), target_square.color)):
                        return True
        
            elif target_square == chessboard[7][7]:
                # Short castling
                if Piece.is_empty(chessboard[7][5]) and Piece.is_empty(chessboard[7][6]) and target_square.moved is False:
                    if not (check_handler.is_square_attacked((7, 5), target_square.color) or check_handler.is_square_attacked((7,6), target_square.color)):
                        return True
        
            return False
        return False

            
    def get_value(self):
        return 0