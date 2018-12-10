import Checkers

def asissert(cond1, cond2):
	if(cond1 != cond2):
		# If error, suffer
		x = 0/0

board = Checkers.Board()

# board.show()

for coord in range (1, 33):
	if board.index_to_coord(board.coord_to_index(coord)) != coord:
		print("FUCKIN")

assert(board.get_hopped_coord(1, 10) == 6)
assert(board.get_hopped_coord(17, 26) == 22)
assert(board.get_hopped_coord(31, 24) == 27)
assert(board.get_hopped_coord(32, 23) == 27)
assert(board.get_hopped_coord(19, 12) == 16)

assert(board.get_nn_output((19, 10))[72])
assert(board.get_nn_output((19, 12))[73])
assert(board.get_nn_output((19, 26))[74])
assert(board.get_nn_output((19, 28))[75])
