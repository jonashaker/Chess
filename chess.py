import board
import pieces

class Chess:

    def __init__(self):
        self.board = board.Board()
        self.move()
        


    def translate(self, location):
        translated_location = [] 
        translated_location.append(int(location.split()[0][0]))
        translated_location.append(int(location.split()[0][2]))
        return translated_location

    def graphical_representation(self):
        pass

    def move(self):
        self.board.printboard()

        while True:
            start = self.translate(input())
            to = self.translate(input())


            if self.board.grid[start[0]][start[1]].is_valid_move(self.board.grid, start, to):
                self.board.grid[to[0]][to[1]] =  self.board.grid[start[0]][start[1]]
                self.board.grid[start[0]][start[1]] = pieces.Empty("free")
                self.board.printboard()
            else:
                print("illegal move")


                



