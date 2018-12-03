#include "Board.h"

Board::Board(int width, int height){
	this->width = width;
	this->height = height;

	this->grid.resize(this->height);
	for(auto it = this->grid.begin(); it != this->grid.end(); ++it) it->resize(this->width, EMPTY_PIECE);

	this->piece_count = 0;
}

void Board::print(){
	for(int r=0; r<this->get_height(); ++r){
		for(int c=0; c<this->get_width(); ++c){
			std::cout << this->get_piece(r, c) << " ";
		}
		std::cout << std::endl;
	}
}

bool Board::remove_piece(int row_i, int col_i){
	if(!valid_grid(row_i, col_i)) return false;
	if(!is_index_occupied(row_i, col_i)) return false;
	this->grid[row_i][col_i] = EMPTY_PIECE;
	this->piece_count--;
	return true;
}
	
Piece Board::get_piece(int row_i, int col_i){
	if(!valid_grid(row_i, col_i)) return EMPTY_PIECE;
	return grid[row_i][col_i];
}

bool Board::place_piece(Piece p, int row_i, int col_i){
	if(!valid_grid(row_i, col_i)) return false;
	if(is_index_occupied(row_i, col_i)) return false;
	this->grid[row_i][col_i] = p;
	this->piece_count++;
	return true;
}

void Board::clear(){
	for(int r=0; r<this->get_height(); ++r){
		for(int c=0; c<this->get_width(); ++c){
			this->remove_piece(r, c);
		}
	}
	this->piece_count = 0;
}

int Board::get_piece_count(){return this->piece_count;}
int Board::get_width(){return this->width;}
int Board::get_height(){return this->height;}

bool Board::valid_grid(int row_i, int col_i){
	if(row_i < 0 || col_i < 0) return false;
	if(row_i >= this->height || col_i >= this->width) return false;
	return true;
}

bool Board::is_index_occupied(int row_i, int col_i){
	return this->grid[row_i][col_i] != EMPTY_PIECE;
}
