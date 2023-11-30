import os
from functions import *
from checkerboard import *
from stats import Stats

'''
Checkers Game
CIS 121 Final Project
Matt - Liam - Trevor
'''

'''Base Variables'''
position_dict = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}  # Converts letter input to a index position
turn = 1           # Which players' turn it is determined by either an odd or even number. Evens are "X", Odds are "O"
error_msg = ""     # If an error occurs, this gets printed
game_over = False  # Game over boolean
total_moves = 0

new_checkerboard = Checkerboard()   # Create a new checkerboard

'''Run Game'''
if startGame():    # Prints all starting messages, and asks for a button press to begin
    while True:    # Run loop


        # Determines player based on turn
        if turn % 2 == 0:
            player = "X"
        else:
            player = "O"


        new_round = Round(player, turn, new_checkerboard.getBoard())               # Initiate a new round
        x_left, o_left, x_kings_left, o_kings_left = new_round.countPieces()  # Count how many of each piece are left


        # If either piece count gets to zero, the other player wins
        if x_left == 0:
            player = "O"
            game_over = True
        elif o_left == 0:
            player = "X"
            game_over = True


        # Print statements for each round
        os.system('cls')                               # Clear the board
        print(f"\033[1m\t      {error_msg}\033[0m")    # Return error message if any
        new_checkerboard.drawBoard()                   # Print board
        print(f"\033[1m\t\tX's: {x_left + x_kings_left}     O's: {o_left + o_kings_left}\033[0m")    # Print how many X's and O's are left
        

        # If game is over, print game over statement
        if game_over:
            print(f"\033[1m{player} wins!\033[0m\n")
            # Make and update a new stats file
            game1 = Stats(total_moves, x_left, o_left, x_kings_left, o_kings_left, player)
            game1.update_file()
            break
        # If game isnt over, print regular player statement
        else:
            print(f"\nYour move player {player}") # Print player statement

    
        get_move = new_round.getMove()    # Get a move from the player, piece and place(s) to move
        if get_move == True:
            if new_round.possibleMove():  # If get move is valid, check if move is possible
                new_round.movePiece()     # If move is possible, move pieces and update the board
            else:
                error_msg = ("Invalid move, try again.")    # If the move wasnt possible, restart loop
                continue
        elif get_move == "quit":    # If a player enters "quit", they forfeit and the other player wins
            game_over = True
        else:
            error_msg = ("Invalid input, try again.")   # If the input was invalid, restart loop
            continue


        # If no errors, make it the next players turn, and reset the error message to blank
        turn += 1
        total_moves += new_round.total_moves
        error_msg = ""
        
