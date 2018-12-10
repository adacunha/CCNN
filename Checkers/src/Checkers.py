import numpy as np

class Board:
	
	def __init__(self):
		self.side_length = 8
		self.refresh()

	def refresh(self):
		self.occupied_squares = {}
		self.unoccupied_squares = set();

		for i in range(1, 33):
			self.unoccupied_squares.add(i)
		
		for i in range(1, 13):
			self.place_own_pawn(1, i)

		for i in range(21, 33):
			self.place_own_pawn(-1, i)

	def place_opponent_pawn(self, player, coord):
		piece = -1 if player == 1 else 1
		self.place_piece(coord, piece)	

	def place_own_pawn(self, player, coord):
		piece = 1 if player == 1 else -1
		self.place_piece(coord, piece)

	def place_opponent_king(self, player, coord):
		piece = -2 if player == 1 else 2
		self.place_piece(coord, piece)

	def place_own_king(self, player, coord):
		piece = 2 if player == 1 else -2
		self.place_piece(coord, piece)

	def place_piece(self, coord, piece):
		self.unoccupied_squares.remove(coord)
		if piece == self.get_black_piece() and coord >= 29:
			piece  = piece * 2
		if piece == self.get_white_piece() and coord <= 4:
			piece = piece * 2
		self.occupied_squares[coord] = piece

	def move_piece(self, coords):
		from_square = coords[0]
		to_square = coords[1]
		piece = self.get_piece(from_square)
		self.remove_piece(from_square)
		self.place_piece(to_square, piece);

	def capture(self, coords):
		start = coords[0]
		end = coords[1]
		piece = self.get_piece(start)
		self.remove_piece(start)
		self.remove_piece(self.get_hopped_coord(start, end))
		self.place_piece(end, piece)

	def get_hopped_coord(self, start_coord, end_coord):
		start_index = self.coord_to_index(start_coord)
		end_index = self.coord_to_index(end_coord)
		delta_x = end_index[0] - start_index[0]
		delta_y = end_index[1] - start_index[1]
		return self.index_to_coord((start_index[0] + int(delta_x/2), start_index[1] + int(delta_y/2)))

	def coord_to_index(self, coord):
		row = int((coord-1)/4)
		col = (coord-1) % 4
		col = col * 2
		if not row&1:
			col = col + 1	
		return (row, col)

	def index_to_coord(self, index):
		row = index[0]
		col = index[1]
		if not row&1:
			col = col - 1	
		col = int(col / 2)
		return 4 * row + (col+1)
	
	def remove_piece(self, coord):
		del self.occupied_squares[coord]
		self.unoccupied_squares.add(coord)

	def get_piece(self, coord):
		if coord in self.occupied_squares:
			return self.occupied_squares[coord];
		return 0

	def get_black_piece(self):
		return 1

	def get_white_piece(self):
		return -1
		
	def show(self):
		print()
		for i in range(0, 32):
			if i != 0 and not i%4 and int(i/4)&1:
				print()
			else:
				print(" ", end='')
			if not i%4 and not int(i/4)&1:
				print()
			print(self.get_piece(i+1), end='')
		print(" ", end='')
		print()
	
	def get_nn_input(self, player):
		return [self.get_piece(i) * player for i in range(1, 33)]

	def get_cnn_input(self, player):
		nn_input = self.get_nn_input(player)
		return np.array([nn_input]).reshape((8, 4, 1));

	def get_nn_output(self, coord):
		from_index = self.coord_to_index(coord[0])
		to_index = self.coord_to_index(coord[1])
		delta_x = to_index[1] - from_index[1]
		delta_y = to_index[0] - from_index[0]
		offset = 0	
		if delta_x > 0 and delta_y < 0:
			offset = 1
		if delta_x < 0 and delta_y > 0:
			offset = 2
		if delta_x > 0 and delta_y > 0:
			offset = 3
		result = [0 for i in range(0, 128)]
		result[(coord[0]-1)*4+offset] = 1
		return result

	def is_valid_index(self, index):
		if index[0] < 0 or index[0] > 7:
			print("Invalid move: Out of board!")
			return False
		if index[1] < 0 or index[1] > 3:
			print("Invalid move: Out of board!")
			return False
		return True

	def parse_nn_output(self, nn_output, player):

		invalid_response = (-1, (-1, -1))

		from_coord = int(nn_output/4)+1

		if from_coord in self.unoccupied_squares:
			print("Invalid move: No Piece at Tile!")
			return invalid_response	

		if self.occupied_squares[from_coord] != player:
			print("Invalid move: Not your piece!")
			return invalid_response

		from_index = self.coord_to_index(from_coord)

		direction = nn_output%4
		delta_x = -1
		delta_y = -1
		if direction == 1 or direction == 3:
			delta_x = 1
		if direction == 2 or direction == 3:
			delta_y = 1

		to_index = (from_index[0]+delta_y, from_index[1]+delta_x)
		
		if not self.is_valid_index(to_index):
			print("Invalid move: Index out of board!")
			return invalid_response

		to_coord = self.index_to_coord(to_index)

		if to_coord in self.unoccupied_squares:
			return (1, (from_coord, to_coord))
		
		if self.occupied_squares[to_coord] == player:
			print("Invalid move: Self capture!")
			return invalid_response	

		to_index = (to_index[0]+delta_y, to_index[1]+delta_x)

		if not self.is_valid_index(to_index):
			print("Invalid capture jump: end index out of board!")
			return invalid_response

		to_coord = self.index_to_coord(to_index)
		return (1, (from_coord, to_coord))
