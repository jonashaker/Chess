class Piece(object):

    def __init__(self):
        pass

    def getName(self):
        return self.__class__.__name__[0:2]

    def is_white(self):
        return self.color == "white"

    def is_black(self):
        return self.color == "black"

    def is_empty(self):
        return self.color == "free"

class Empty(Piece):
    def __init__(self, color):
        super().__init__()
        self.color = color


class Pawn(Piece):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        """ Start, to: Zeroth Index, Row. First Index, Column. """
        goal = grid[to[0]][to[1]]
        if Piece.is_white(self):
            if abs(start[1]-to[1]) == 1:
                # White tries to defeat an enemy with a pawn
                if to[0]-start[0] == 1:
                    return Piece.is_black(goal)
                else:
                    return False
            elif to[1] == start[1]:
                # White tries to advance straight with pawn
                if to[0]-start[0] == 1:
                    return Piece.is_empty(goal)
                else:
                    return False
            else:
                return False
        else:
            if abs(start[1]-to[1]) == 1:
                # Black tries to defeat an enemy with a pawn
                if to[0]-start[0] == -1:
                    return Piece.is_white(goal)
                else:
                    return False
            elif to[1] == start[1]:
                # Black tries to advance straight with pawn
                if to[0]-start[0] == -1:
                    return Piece.is_empty(goal)
                else:
                    return False
            else:
                return False



class Rook(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]
        if start[0] == to[0]:
            # Rook moves sideways
            if abs(to[1]-start[1]) >= 2:
                # Empty spaces between initial position and goal
                for i in range(min(start[1], to[1])+1,max(start[1], to[1])):
                    if not Piece.is_empty(grid[to[0]][i]):
                        return False

            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)

        elif start[1] == to[1]:
            # Rook moves forward/backwards
            if abs(to[0]-start[0]) >= 2:
                # Empty spaces between initial position and goal
                for i in range(min(start[0], to[0])+1,max(start[0], to[0])):
                    if not Piece.is_empty(grid[i][to[1]]):
                        return False

            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)
        else:
            return False


class Bishop(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]
        if abs(to[0]-start[0]) == abs(to[1]-start[1]):
            # Legal move
            if abs(to[1]-start[1]) >= 2:
                # Empty positions between start and goal. Four cases:
                if to[0] > start[0] and to[1] > start[1]:
                    # Move down right
                    for i in range(1, abs(to[1]-start[1])):
                        if not Piece.is_empty(grid[start[0] + i][start[1] + i]):
                            return False
                elif to[0] > start[0] and to[1] < start[1]:
                    # Move down left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] + i][start[1] - i]):
                            return False
                elif to[0] < start[0] and to[1] > start[1]:
                    # Move up right
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] - i][start[1] + i]):
                            return False
                else:
                    # Move up left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] - i][start[1] - i]):
                            return False

            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)
        else:
            return False


class Knight(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]
        if abs(to[0]-start[0]) == 2 and abs(to[1]-start[1]) == 1 or abs(to[0]-start[0]) == 1 and abs(to[1]-start[1]) == 2:
            # Legal move
            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)
        else:
            return False
   

class Queen(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]
        if start[0] == to[0] or start[1] == to[1]:
            # Move as rook
            if start[0] == to[0]:
                # Rook moves sideways
                if abs(to[1]-start[1]) >= 2:
                    # Empty spaces between initial position and goal
                    for i in range(min(start[1], to[1])+1,max(start[1], to[1])):
                        if not Piece.is_empty(grid[to[0]][i]):
                            return False

                if Piece.is_white(self):
                    return not Piece.is_white(goal)
                else:
                    return not Piece.is_black(goal)

            elif start[1] == to[1]:
                # Rook moves forward/backwards
                if abs(to[0]-start[0]) >= 2:
                    # Empty spaces between initial position and goal
                    for i in range(min(start[0], to[0])+1,max(start[0], to[0])):
                        if not Piece.is_empty(grid[i][to[1]]):
                            return False

                if Piece.is_white(self):
                    return not Piece.is_white(goal)
                else:
                    return not Piece.is_black(goal)
            else:
                return False
                
        elif abs(to[0]-start[0]) == abs(to[1]-start[1]):
            # Move as Bishop
            if abs(to[1]-start[1]) >= 2:
                # Empty positions between start and goal. Four cases:
                if to[0] > start[0] and to[1] > start[1]:
                    # Move down right
                    for i in range(1, abs(to[1]-start[1])):
                        if not Piece.is_empty(grid[start[0] + i][start[1] + i]):
                            return False
                elif to[0] > start[0] and to[1] < start[1]:
                    # Move down left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] + i][start[1] - i]):
                            return False
                elif to[0] < start[0] and to[1] > start[1]:
                    # Move up right
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] - i][start[1] + i]):
                            return False
                else:
                    # Move up left
                    for i in range(1, abs(to[1] - start[1])):
                        if not Piece.is_empty(grid[start[0] - i][start[1] - i]):
                            return False

            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)
        else:
            return False

class King(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]

        # Four cases
        if abs(start[0]-to[0]) <= 1 and abs(start[1]-to[1]) <= 1:
            if Piece.is_white(self):
                return not Piece.is_white(goal)
            else:
                return not Piece.is_black(goal)
        else:
            return False
