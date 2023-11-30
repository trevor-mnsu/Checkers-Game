from tabulate import tabulate

# Base checkerboard array
class Checkerboard:
    def __init__(self):
        self.board = [
            ["O"," ","O"," ","O"," ","O"," "],
            [" ","O"," ","O"," ","O"," ","O"],
            ["O"," ","O"," ","O"," ","O"," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" ","X"," ","X"," ","X"," ","X"],
            ["X"," ","X"," ","X"," ","X"," "],
            [" ","X"," ","X"," ","X"," ","X"],
            ]

    # Print board using tabulate
    def drawBoard(self):
        # List of letters A-G,each letter being bolded
        rowIDs = ["\033[1mA\033[0m","\033[1mB\033[0m","\033[1mC\033[0m","\033[1mD\033[0m","\033[1mE\033[0m","\033[1mF\033[0m","\033[1mG\033[0m","\033[1mH\033[0m"]
        # List of numbers 1-8 being bolded
        headers = ["\033[1m1","2","3","4","5","6","7","8\033[0m"]
        print(tabulate(self.board,tablefmt="simple_grid",showindex=rowIDs,headers=headers,stralign="center"))

    def getBoard(self):
        return self.board
    
