#ifndef __TTTBOARD_H_
#define __TTTBOARD_H_

#include "Board.h"

#define X 1
#define EMPTY_PIECE 0
#define O -1

#define TTT_BOARD_SIZE 3

class TTTBoard : public Board {
	public:
		TTTBoard() : Board(TTT_BOARD_SIZE, TTT_BOARD_SIZE) {
		}
		bool place_X(int row_i, int col_i){
			return this->place_piece(X, row_i, col_i);
		}	
		bool place_O(int row_i, int col_i){
			return this->place_piece(O, row_i, col_i);
		}
		bool O_victor(){
			return consecutive_count(O, 3);		
		}			
		bool X_victor(){
			return consecutive_count(X, 3);
		}
		bool is_drawn(){
			if(this->O_victor() || this->X_victor()) return false;
			return this->get_piece_count() == TTT_BOARD_SIZE*TTT_BOARD_SIZE;
		}
		std::vector<std::vector<std::vector<int>>> get_empty_cnn_input(){
			std::vector<std::vector<std::vector<int>>> layer(2, std::vector<std::vector<int>>(TTT_BOARD_SIZE, std::vector<int>(TTT_BOARD_SIZE, 0)));
			return layer;
		}
		void fill_cnn_input_X(std::vector<std::vector<std::vector<int>>>& input_layer){
			fill_cnn_input(X, input_layer);
		}
		void fill_cnn_input_O(std::vector<std::vector<std::vector<int>>>& input_layer){
			fill_cnn_input(O, input_layer);
		}
		void print_layer(std::vector<std::vector<std::vector<int>>>& layer){
			std::cout << std::endl;
			for(int l=0; l<layer.size(); ++l){
				std::cout << "Layer: " << l << std::endl;
				for(int r=0; r<layer[0].size(); ++r){
					for(int c=0; c<layer[0][0].size(); ++c){
						std::cout << layer[l][r][c] << " ";
					}
					std::cout << std::endl;
				}
			}
			std::cout << std::endl;
		}
		void print_cnn_layers(){
			std::vector<std::vector<std::vector<int>>> layer = this->get_empty_cnn_input();
			std::cout << "X Layer: " << std::endl;
			this->fill_cnn_input_X(layer);
			print_layer(layer);	
			std::cout << "O Layer: " << std::endl;
			this->fill_cnn_input_O(layer);
			print_layer(layer);
		}
	private:
		bool consecutive_count(Piece p, int count){
			for(int i = 0; i < TTT_BOARD_SIZE; ++i){
				Piece row_match = this->get_piece(i, 0);
				Piece col_match = this->get_piece(0, i);
				
				bool row_valid = row_match == p;
				bool col_valid = col_match == p;
				for(int j=1; j < TTT_BOARD_SIZE; ++j){
					if(this->get_piece(i, j) != row_match) row_valid = false;
					if(this->get_piece(j, i) != col_match) col_valid = false;
				}
				if(row_valid || col_valid) return true;
			}
			Piece diag_match_left = this->get_piece(0, 0);
			Piece diag_match_right = this->get_piece(TTT_BOARD_SIZE-1, TTT_BOARD_SIZE-1);
			bool diag_valid_left = diag_match_left == p;
			bool diag_valid_right = diag_match_right == p;
			for(int i=1; i<TTT_BOARD_SIZE; ++i){
				if(this->get_piece(i, i) != diag_match_left) diag_valid_left = false;
				if(this->get_piece(i, TTT_BOARD_SIZE-1-i) != diag_match_right) diag_valid_right = false;
			}
			return diag_valid_left || diag_valid_right;
		}
		void fill_cnn_input(Piece player_piece, std::vector<std::vector<std::vector<int>>>& input_layer){
			for(int r=0; r<TTT_BOARD_SIZE; ++r){
				for(int c=0; c<TTT_BOARD_SIZE; ++c){
					Piece p = this->get_piece(r, c);
					input_layer[0][r][c] = p == player_piece;
					input_layer[1][r][c] = p != EMPTY_PIECE && p != player_piece;
				}
			}	
		}
};

#endif
