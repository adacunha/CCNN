
import TTT

board = TTT.Board(3);

data_file = open("games_train.dat", "a")
board.log_to(data_file)

training_size = 10

start_player = 1
for i in range(0, training_size):
	board.refresh()
	current_player = start_player
	start_player *= -1
	while(not board.has_won() and not board.drawn()):
		best_play = board.negamax(current_player)
		board.place_piece(best_play[1][0], best_play[1][1], current_player)
		current_player *= -1
