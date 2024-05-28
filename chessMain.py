"""
This is the main driver file
It will be responsible for handling user input and displaying the current GameState object
"""
import pygame as p
import chessEngine

WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimensions of the chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION 
MAX_FPS = 15 #for animations
IMAGES = {}

'''
Initialize a global dictionary of images
This will be called exactly once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #we can access an image by saying 'IMAGES['wp']'

''' Highlight square selected and moves for piece selected '''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(130) #transparency value -> 0 transparent; 255 -> opaque
            s.fill(p.Color('dark blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c: #then that move is starting from our selected square
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of those squares

'''
Draw the squares on the board
The top left square is always light
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("dark green")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Draw the pieces on the board using the current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

''' Animating a move '''
def animateMove(move, screen, board, clock):
    global colors
    deltaR = move.endRow - move.startRow
    deltaC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(deltaR) + abs(deltaC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + deltaR*frame/frameCount, move.startCol + deltaC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

'''
The main driver for our code
Will handle user input and updating the graphics
'''
def main():
    p.init() #initialize pygame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when we should animate a move
    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected initially, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6,4), (4,4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after the 2nd click
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            animate = True
                            sqSelected = () #reset user clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo move when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r: #reset board when 'r' is pressed
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()