#ifndef __TTTBOARD_H_
#define __TTTBOARD_H_

#include "Board.h"

// Using integers to represent pieces 
#define X 1
#define EMPTY_PIECE 0
#define O -1

#define TTT_BOARD_SIZE 3

class TTTBoard : public Board {

	public:

		TTTBoard();
		
		// Generic TicTacToe Utilities
		bool place_X(int row_i, int col_i);
		bool place_O(int row_i, int col_i);
		bool O_victor();
		bool X_victor();
		bool is_drawn();

		// Methods for CNN Interoperability
		std::vector<std::vector<std::vector<int>>> get_empty_cnn_input();
		void fill_cnn_input_X(std::vector<std::vector<std::vector<int>>>& input_layer);
		void fill_cnn_input_O(std::vector<std::vector<std::vector<int>>>& input_layer);
		void print_layer(std::vector<std::vector<std::vector<int>>>& layer);
		void print_cnn_layers();

	private:

		// To check for win condition
		bool consecutive_count(Piece p, int count);

		// Create board state readable by Convolutional Neural Network
		void fill_cnn_input(Piece player_piece, std::vector<std::vector<std::vector<int>>>& input_layer);
};

#endif
