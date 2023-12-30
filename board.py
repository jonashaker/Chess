import pieces


class Board:

    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]

        self.grid[0][0] = pieces.Rook("white")
        self.grid[0][1] = pieces.Knight("white")
        self.grid[0][2] = pieces.Bishop("white")
        self.grid[0][3] = pieces.Queen("white")
        self.grid[0][4] = pieces.King("white")
        self.grid[0][5] = pieces.Bishop("white")
        self.grid[0][6] = pieces.Knight("white")
        self.grid[0][7] = pieces.Rook("white")

        self.grid[7][0] = pieces.Rook("black")
        self.grid[7][1] = pieces.Knight("black")
        self.grid[7][2] = pieces.Bishop("black")
        self.grid[7][3] = pieces.Queen("black")
        self.grid[7][4] = pieces.King("black")
        self.grid[7][5] = pieces.Bishop("black")
        self.grid[7][6] = pieces.Knight("black")
        self.grid[7][7] = pieces.Rook("black")

        for column in range(8):
            self.grid[1][column] = pieces.Pawn("white")
            self.grid[6][column] = pieces.Pawn("black")

        for row in range(2,6):
            for column in range(8):
                self.grid[row][column] = pieces.Empty("free")


    def printboard(self):

        for row in range(8):
            str = ""
            for column in range(8):
                pos = self.grid[row][column]
                str += "|" + pos.color + " " + pos.getName()
            str += "|"
            print(str)






