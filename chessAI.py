import random

pieceScores = {"K" : 0, "Q" : 10, "R": 5, "B" : 3, "N" : 3, "p" : 1} #responsible for assigning a point value for each piece
CHECKMATE = 1000
STALEMATE = 0


''' Picks and returns a random move '''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

''' Find the best move based on material alone (greedy algorithm and minmax without recursion)'''
def findGreedyMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 #var to say if it's black turn or whites turn => will help determine whether to maximize or minimize the board
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves: 
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score = -turnMultiplier * CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

''' Score the board based on material '''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    return score