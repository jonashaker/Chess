import pieces

chessboard = [[pieces.Rook("white"), pieces.Knight("white"), pieces.Bishop("white"), pieces.Queen("white"), pieces.King("white"), pieces.Bishop("white"), pieces.Knight("white"), pieces.Rook("white")],
              [pieces.Pawn("white")]*8,
              [pieces.Empty(None)]*8,
              [pieces.Empty(None)]*8,
              [pieces.Empty(None)]*8,
              [pieces.Empty(None)]*8,
              [pieces.Pawn("black")]*8,
              [pieces.Rook("black"), pieces.Knight("black"), pieces.Bishop("black"), pieces.Queen("black"), pieces.King("black"), pieces.Bishop("black"), pieces.Knight("black"), pieces.Rook("black")]]


def castling(chessboard, start, to):
    # Castling 
        if abs(start[1]-to[1]) == 3:
            # Short castling
            chessboard[to[0]][to[1]-1] = chessboard[start[0]][start[1]]
            chessboard[to[0]][to[1]-2] = pieces.Rook("%s" % chessboard[start[0]][start[1]].color)
        else:
            # Long castling
            chessboard[to[0]][to[1]+2] = chessboard[start[0]][start[1]]
            chessboard[to[0]][to[1]+3] = pieces.Rook("%s" % chessboard[start[0]][start[1]].color)

        chessboard[start[0]][start[1]] = pieces.Empty(None)
        chessboard[to[0]][to[1]] = pieces.Empty(None)

        return chessboard

def en_passant(chessboard, start, to):
    if chessboard[start[0]][start[1]].color == "white":
        chessboard[to[0]-1][to[1]] = pieces.Empty(None)
    else:
        chessboard[to[0]+1][to[1]] = pieces.Empty(None)
    
    return chessboard

def create_pseudo_pawns(chessboard, start, to):
    # Create pseudo pawn
        if chessboard[start[0]][start[1]].color == "white":
            chessboard[start[0]+1][start[1]] = pieces.Pseudo_Pawn()
        else:
            chessboard[start[0]-1][start[1]] = pieces.Pseudo_Pawn()

        return chessboard

def promotion(chessboard, start, to):
    chessboard[to[0]][to[1]] = pieces.Queen("%s" % chessboard[start[0]][start[1]].color)
    chessboard[start[0]][start[1]] = pieces.Empty(None)
    return chessboard


def update_board(chessboard, start, to):

    """Implements regular moves and the three special rules: Castling, pawn promotion and en passant."""
    
    if abs(to[0]-3.5) == 3.5 and chessboard[start[0]][start[1]].getName() == "Pawn":
        # Promote pawn
        return promotion(chessboard, start, to)
    
    
    if chessboard[start[0]][start[1]].getName() == "King" and chessboard[to[0]][to[1]].getName() == "Rook":
        # Castling
        return castling(chessboard, start, to)
    
    
    if chessboard[start[0]][start[1]].getName() == "Pawn" and chessboard[to[0]][to[1]].getName() == "Pseudo_Pawn":
        chessboard = en_passant(chessboard, start, to)
    
    for col in range(8):
        if chessboard[2][col].getName() == "Pseudo_Pawn":
            chessboard[2][col] = pieces.Empty(None)

        if chessboard[5][col].getName() == "Pseudo_Pawn":
            chessboard[5][col] = pieces.Empty(None) 
    

    if chessboard[start[0]][start[1]].getName() == "Pawn" and abs(to[0]-start[0]) == 2:
        
        chessboard = create_pseudo_pawns(chessboard, start, to)
        
    chessboard[to[0]][to[1]] = chessboard[start[0]][start[1]]
    chessboard[start[0]][start[1]] = pieces.Empty(None)
    return chessboard

def check(chessboard):
    pass





