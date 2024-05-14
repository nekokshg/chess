"""
This class is responsible for storing all the info about the current state of a chess game
It will also be responsible for determining the valid moves at the current state
It will also keep a move log
"""
class GameState():
    def __init__(self):
        #board is an 8x8 2D list with each element of the list having 2 char
        #the first char represents the color of the piece, 'b' or 'w'
        #the second char represents the type of the piece, 'K' 'Q' 'R' 'B' 'N' 'p'
        #'--' represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]