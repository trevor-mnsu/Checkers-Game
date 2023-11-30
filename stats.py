class Stats:
    def __init__(self, total_moves, x_left, o_left, x_kings_left, o_kings_left, winner):
        self.total_moves = str(total_moves)
        self.x_kings_left = str(x_kings_left)
        self.o_kings_left = str(o_kings_left)
        self.x_left = str(x_left)
        self.o_left = str(o_left)
        self.winner = str(winner)
    
    def update_file(self):
        with open("stats.csv", "w") as stats_file:
            stats_file.write(
                "moves made in total, x(s) left, o(s) left, x king(s) left, o king(s) left, winner\n"
                f"{self.total_moves}, {self.x_left}, {self.o_left}, {self.x_kings_left}, {self.o_kings_left}, {self.winner}"
                            )
