class Piece(object):

    def __init__(self):
        pass

    def getName(self):
        return self.__class__.__name__

    def is_white(self):
        return self.color == "white"

    def is_black(self):
        return self.color == "black"

    def is_empty(self):
        return self.color is None

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
                    return Piece.is_black(goal) or Piece.getName(goal) == "Pseudo_Pawn"
                else:
                    return False
            elif to[1] == start[1]:
                # White tries to advance straight with pawn
                if to[0]-start[0] == 1:
                    return Piece.is_empty(goal)
                elif start[0] == 1 and to[0]-start[0] == 2:
                    return (Piece.is_empty(goal) and Piece.is_empty(grid[to[0]-1][to[1]]))
                else:
                    return False
            else:
                return False
        else:
            if abs(start[1]-to[1]) == 1:
                # Black tries to defeat an enemy with a pawn
                if to[0]-start[0] == -1:
                    return Piece.is_white(goal) or Piece.getName(goal) == "Pseudo_Pawn"
                else:
                    return False
            elif to[1] == start[1]:
                # Black tries to advance straight with pawn
                if to[0]-start[0] == -1:
                    return Piece.is_empty(goal)
                elif start[0] == 6 and to[0]-start[0] == -2:
                    return (Piece.is_empty(goal) and Piece.is_empty(grid[to[0]+1][to[1]]))
                else:
                    return False
            else:
                return False

class Pseudo_Pawn(Piece):

    def __init__(self):
        super().__init__()
        self.color = None

class Rook(Piece):

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.moved = False

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
                if not Piece.is_white(goal):
                    self.moved = True
                    return True
            else:
                if not Piece.is_black(goal):
                    self.moved = True
                    return True

        elif start[1] == to[1]:
            # Rook moves forward/backwards
            if abs(to[0]-start[0]) >= 2:
                # Empty spaces between initial position and goal
                for i in range(min(start[0], to[0])+1, max(start[0], to[0])):
                    if not Piece.is_empty(grid[i][to[1]]):
                        return False

            if Piece.is_white(self):
                if not Piece.is_white(goal):
                    self.moved = True
                    return True
            else:
                if not Piece.is_black(goal):
                    self.moved = True
                    return True
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
        self.moved = False

    def is_valid_move(self, grid, start, to):
        goal = grid[to[0]][to[1]]

        # Four cases
        if abs(start[0]-to[0]) <= 1 and abs(start[1]-to[1]) <= 1:
            if Piece.is_white(self):
                if not Piece.is_white(goal):
                    self.moved = True
                    return True
            else:
                if not Piece.is_black(goal):
                    self.moved = True
                    return True
            return False
            
        elif self.moved == False and Piece.is_white(self):
            # White tries to castle
            if goal == grid[0][0]:
                if Piece.is_empty(grid[0][1]) and Piece.is_empty(grid[0][2]) and Piece.is_empty(grid[0][3]) and goal.moved is False:
                    self.moved = True
                    return True
                
            elif goal == grid[0][7]:
                if Piece.is_empty(grid[0][5]) and Piece.is_empty(grid[0][6]) and goal.moved is False:
                    self.moved = True
                    return True
                
            return False
        
        elif self.moved == False and Piece.is_black(self):
            # Black tries to castle
            if goal == grid[7][0]:
                if Piece.is_empty(grid[7][1]) and Piece.is_empty(grid[7][2]) and Piece.is_empty(grid[7][3]) and goal.moved is False:
                    self.moved = True
                    return True
        
            elif goal == grid[7][7]:
                if Piece.is_empty(grid[7][5]) and Piece.is_empty(grid[7][6]) and goal.moved is False:
                    self.moved = True
                    return True
            
            return False

            
