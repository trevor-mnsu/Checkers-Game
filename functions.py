from checkerboard import *

'''Start Game'''
def startGame():
    # Starting message and directions
    msg = [
            ["Welcome to Checkers: The Bootleg Edition"], 
            ["When prompted, select a piece (eg. C1)."
             "\nThen enter the move (eg. D2), if you wish to jump multiple pieces enter as following, (eg. E3 G5)"
             '\nIf you are unable to move, or wish to forfeit, enter "quit".'
             ]
           ]
    
    # Prints the board using the "Tabulate" module
    print(tabulate(msg, tablefmt="simple_grid"))

    # Asks for an input to begin the game
    start = input("  Press enter to begin: ")
    if start == "":
        return True


'''Round Class'''
class Round:
    # Each turn or round of the game, this class gets updated

    '''Constructor Function'''
    def __init__(self, player, turn, board):
        self.position_dict = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}  # Converts letter input to a index position
        self.piece = "B2"      # Piece selected
        self.moves = []        # Moves entered
        self.player = player   # Player (O or X)
        self.board = board     # Checkerboard
        self.turn = turn       # Turn count
        self.cr = 0   # Current Row Selected
        self.cc = 0   # Current Col Selected
        self.orr = 0  # Original Row Entered
        self.orc = 0  # Original Column Entered
        self.total_moves = 0
        # Need an original row and col saved because the current row and col needs to be updated later in order to loop through the moves

    
    '''Count Pieces'''
    def countPieces(self):
        x_left, o_left, x_kings_left, o_kings_left = 0,0,0,0
        # For each row in the board, count the pieces and return them all
        for row in self.board:
            x_left += row.count("X")
            o_left += row.count("O")
            x_kings_left += row.count("K")
            o_kings_left += row.count("Q")
        return x_left, o_left, x_kings_left, o_kings_left


    '''Get Move'''
    def getMove(self):
        # Update all variables
        self.piece = input("\n    Enter Piece: ")  # Select a piece

        if self.piece == "quit":    # If "quit" is entered, player forfeits
            return "quit"
        
        self.moves = input("    Enter Move: ").split(" ")  # Enter however many moves to be made. Each move is entered into a list
        
        # All inputs need to be valid before updating the cr, cc, orr, and orc; in order to avoid errors
        if self.validInput():
            self.cr = int(self.position_dict[self.piece[0].upper()])    # Returns corresponding board index for the letter that is given
            self.cc = int(self.piece[1]) - 1                            # Returns 1 less than the number entered to align with the 0 index system
            self.orr = int(self.position_dict[self.piece[0].upper()])  
            self.orc = int(self.piece[1]) - 1
            return True
        else:
            return False


    '''Valid Input Function'''
    def validInput(self):
        # Checks if all inputs are valid
        for move in self.moves:
            # If inputs are not the correct length, or include invalid characters, return False
            if (
                ((len(self.piece) == 2) and (self.piece[0].upper() in "ABCDEFGH") and (self.piece[1] in "12345678")
                and (len(move) == 2) and (move[0].upper() in "ABCDEFGH") and (move[1] in "12345678"))
                ):
                return True
            else:
                return False


    '''Update Moves List'''
    def updateMoves(self):
        # Changes each move in the "moves" list into a properly indexed move (eg. "A1" == [0,0]), to be used in later functions
        for i in range(len(self.moves)):
            move = [self.moves[i][0],self.moves[i][1]]    # Split letter and num into a list
            move[0], move[1] = self.position_dict[move[0].upper()], int(move[1]) - 1    # Change letter and num into corresponding index pos
            self.moves[i] = move    # Re-append the indexed move into the "moves" list


    '''In Bounds'''
    def inBounds(self, nr, nc):
        # Makes sure the play is in bounds of the board, the space is empty, and the player is playing correct pieces
        if(
            0 <= self.cr < 8
            and 0 <= self.cc < 8        
            and 0 <= nr < 8        
            and 0 <= nc < 8
            and self.board[nr][nc] == " "     # Makes sure new spot is empty
            and self.same(self.orr, self.orc) # Makes sure the player is playing his own piece
        ):
            return True
        else:
            return False
        

    '''Determine Same Pieces'''
    def same(self, row, col):
        # If the player is X, and the piece he is selecting is either an "X" or a "K", return True; vice versa for player O
        if ((self.player == "X" and (self.board[row][col] == "X" or self.board[row][col] == "K"))
            or (self.player == "O" and (self.board[row][col] == "O" or self.board[row][col] == "Q"))):
            return True
        else:
            return False
        

    '''Determines Jumped Piece'''
    def jumpedPiece(self, nr, nc):
        # Returns the place on the checkerboard between the current position and the new position
        if nr > self.cr:
            if nc > self.cc:
                jumped_piece = [nr-1, nc-1]
            else:
                jumped_piece = [nr-1, self.cc-1]
        else:                                 
            if nc > self.cc:
                jumped_piece = [self.cr-1, nc-1]
            else:
                jumped_piece = [self.cr-1, self.cc-1]
        return jumped_piece


    '''Determine Possible Move'''
    def possibleMove(self):
        # Possible moves for each piece type, based on index positions. (eg. +1,+1 from cr, cc)
        o_moves = ((1,1),(1,-1),(2,2),(2,-2))
        x_moves = ((-1,1),(-1,-1),(-2,2),(-2,-2))
        king_moves = ((1,1),(1,-1),(-1,1),(-1,-1),(2,2),(2,-2),(-2,2),(-2,-2))
        self.updateMoves()    # Update the moves list to be used for the loop

        for nr, nc in self.moves:    # For each [nr, nc]] in the self.moves list, check if all things are valid
            change_in_position = (nr-self.cr,nc-self.cc)    # Change between current position and new position

            if self.inBounds(nr,nc):    # If in bounds
                # If theres a jump. If the jumped piece is of the same team, or there is no piece being jumped, return False
                if self.isJump(change_in_position):
                    jumped_piece = self.jumpedPiece(nr,nc)
                    if (self.same(jumped_piece[0],jumped_piece[1]) or self.board[jumped_piece[0]][jumped_piece[1]] == " "):
                        return False
                # If the move that is entered is not within the lists of possible moves, return False
                if self.board[self.cr][self.cc] == "X":
                    if change_in_position not in x_moves:
                        return False
                elif self.board[self.cr][self.cc] == "O":
                    if change_in_position not in o_moves:
                        return False
                elif self.board[self.cr][self.cc] == "K" or self.board[self.cr][self.cc] == "Q":
                    if change_in_position not in king_moves:
                        return False
            else:
                return False
            self.cr, self.cc = nr, nc   # Update the current row and col to where the piece was "moved" too

        return True    # If nothing is invalid, return True
            

    '''Is Jump'''
    def isJump(self, change_in_position):
        if abs(change_in_position[0]) == 2: # If the change in position contains a 2, its a jump
            return True


    '''Determining King Pieces'''
    def isKing(self,nr):
        # If an "X" or "O" reaches the opposite end of the board, return True
        if (self.board[self.cr][self.cc] == "X" and nr == 0) or (self.board[self.cr][self.cc] == "O" and nr == 7):
            return True
        else:
            return False


    '''Move Piece Function'''
    def movePiece(self):
        self.cr, self.cc = self.orr, self.orc   # Reset the current row and current col back to the original entry

        for nr, nc in self.moves:    # For each move[new_row, new_col] in the "self.moves" list, move the piece
            change_in_position = (nr-self.cr,nc-self.cc)

            if self.isKing(nr):    # If a piece reaches the other, make it a "king"
                if self.player == "X":
                    self.board[self.cr][self.cc] = " "
                    self.board[nr][nc] = "K"
                else: 
                    self.board[self.cr][self.cc] = " "
                    self.board[nr][nc] = "Q"
            # Replaces current position with a space, and new position with the checker
            else:
                self.board[nr][nc] = self.board[self.cr][self.cc]   # Move current piece to new position
                self.board[self.cr][self.cc] = " "    # Reset original position to blank
            if self.isJump(change_in_position):    # If there is a jump
                jumped_piece = self.jumpedPiece(nr,nc)  # Gets the position of the piece being jumped
                self.board[jumped_piece[0]][jumped_piece[1]] = " "  # "Kill" this piece between the current and new position

            self.cr, self.cc = nr, nc   # Update the current row and col to where the piece was "moved" too
            self.total_moves += 1       # Add one to total moves made
