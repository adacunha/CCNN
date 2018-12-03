#include "Test.h"

void test_TTTBoard(){

	bool t = 1;
	TTTBoard b;

	assert_equals(b.O_victor(), 0, "initial win condition");
	assert_equals(b.X_victor(), 0, "initial win condition");

	assert_equals(b.place_O(0, 0), 1, "initial place condition");
	assert_equals(b.place_O(1, 1), 1, "initial place condition");
	assert_equals(b.place_O(2, 2), 1, "initial place_condition");

	assert_equals(b.O_victor(), 1, "left diag win condition");
	assert_equals(b.X_victor(), 0, "left diag win condition FALSE");
	
	assert_equals(b.place_O(1, 1), 0, "invalid place condition");
	assert_equals(b.O_victor(), 1, "invalid place invariant");
	assert_equals(b.X_victor(), 0, "invalid place invariant");

	assert_equals(b.remove_piece(1, 1), 1, "remove piece");
	assert_equals(b.remove_piece(1, 1), 0, "remove missing piece");
	assert_equals(b.O_victor(), 0, "victor voided condition");
	assert_equals(b.X_victor(), 0, "victor voided condition");

	assert_equals(b.place_X(1, 1), 1, "place condition");
	assert_equals(b.O_victor(), 0, "place victor condition");
	assert_equals(b.X_victor(), 0, "place victor condition");

	assert_equals(b.remove_piece(1, 1), 1, "remove piece condition 1");
	assert_equals(b.remove_piece(2, 2), 1, "remove piece condition 2");
	assert_equals(b.remove_piece(0, 0), 1, "remove piece condition 3");

	for(int i=0; i<3; ++i){
		for(int j=0; j<3; ++j){
			assert_equals(b.place_X(i, j), 1, "place piece bulk");
		}
	}
	assert_equals(b.is_drawn(), false, "drawn when won");
	
	b.clear();
	assert_equals(b.get_piece_count(), 0, "clear test");

	b.place_O(0, 0);
	b.place_O(1, 0);
	b.place_O(0, 2);
	b.place_X(0, 1);
	b.place_X(2, 0);
	b.place_O(2, 1);
	b.place_X(1, 2);
	b.place_X(2, 2);
	b.place_O(1, 1);
	b.place_O(2, 1);

	assert_equals(b.X_victor(), false, "x draw test");
	assert_equals(b.O_victor(), false, "o draw test");
	assert_equals(b.is_drawn(), true, "drawn test");
	assert_equals(b.get_piece_count(), 9, "bulk piece count");

	b.clear();

	std::vector<std::vector<std::vector<int>>> cnn_input;
	
	cnn_input = b.get_empty_cnn_input();
	assert_equals(cnn_input.size(), 2, "cnn input layers");
	assert_equals(cnn_input[0].size(), 3, "cnn input layer width");
	assert_equals(cnn_input[0][0].size(), 3, "cnn input layer height");
	
	b.fill_cnn_input_X(cnn_input);

	for(int l=0; l<2; ++l){
		for(int r=0; r<3; ++r){
			for(int c=0; c<3; ++c){
				assert_equals(cnn_input[l][r][c], EMPTY_PIECE, "cnn_default_empty");	
			}
		}		
	}

	b.place_O(0, 0);
	b.place_O(1, 0);
	b.place_O(0, 2);
	b.place_X(0, 1);
	b.place_X(2, 0);
	b.place_O(2, 1);
	b.place_X(1, 2);
	b.place_X(2, 2);
	b.place_O(1, 1);

	b.fill_cnn_input_X(cnn_input);
	for(int l=0; l<2; ++l){
		for(int r=0; r<3; ++r){
			for(int c=0; c<3; ++c){
				if(!l && cnn_input[l][r][c]) assert_equals(b.get_piece(r, c), X, "cnn layer 0 match");	
				if(l==1 && cnn_input[l][r][c]) assert_equals(b.get_piece(r, c), O, "cnn layer 1 match");	
			}
		}		
	}
	
}

void test_Board(){
	Board b(10, 5);
	assert_equals(b.get_piece_count(), 0, "board piece count");
	assert_equals(b.get_width(), 10, "board width");
	assert_equals(b.get_height(), 5, "board height");
	assert_equals(b.place_piece(1, 1, 1), 1, "board place");
	assert_equals(b.get_piece_count(), 1, "board count");
	assert_equals(b.place_piece(1, 1, 1), 0, "board place");
	assert_equals(b.get_piece_count(), 1, "board count");
	assert_equals(b.remove_piece(1, 1), 1, "board remove");
	assert_equals(b.remove_piece(1, 1), 0, "board remove2");
	assert_equals(b.get_piece_count(), 0, "board count");
}

void test_matrix_util(){
	std::vector<std::vector<double>> A = {
		{1, 2},
		{3, 4},
		{5, 6}
	};
	std::vector<std::vector<double>> A_T = {
		{1, 3, 5},
		{2, 4, 6}
	};
	std::vector<std::vector<double>> B = {
		{1, 2},
		{3, 4}		   
	};
	std::vector<std::vector<double>> B_T = {
		{1, 3},
		{2, 4}
	};
	std::vector<std::vector<double>> a_b = {
		{7, 10},
		{15, 22},
		{23, 34}
	};

	std::vector<std::vector<double>> A_t = matrix_transpose(A);
	std::vector<std::vector<double>> B_t = matrix_transpose(B);
	
	if(A_t != A_T){
		std::cout << "MESSED UP TRANSPOSE:" << std::endl;
		print_matrix(A);
		print_matrix(A_t);
	}	

	if(B_t != B_T){
		std::cout << "MESSED UP TRANSPOSE:" << std::endl;
		print_matrix(B);
		print_matrix(B_t);
	}	

	std::vector<std::vector<double>> A_B = matrix_mult(A, B);
	if(A_B != a_b){
		std::cout << "MESSED UP MATRIX MULT!" << std::endl;
		print_matrix(A);
		print_matrix(B);
		print_matrix(a_b);
	}	

}

void test_NN(){
	NN nn({1, 100, 100, 1});
	
	int train_size = 10000;
	int test_size = 1000;
	std::vector<std::vector<double>> train_data(train_size, std::vector<double>(1));
	std::vector<std::vector<double>> train_labels(train_size, std::vector<double>(1));
	for(int i=0; i<train_size; ++i){
		double rand_x = (rand() % 10000)/5000.0 - 1;
		train_data[i][0] = rand_x;
		train_labels[i][0] = std::sin(rand_x);
	}

	std::vector<std::vector<double>> test_data(test_size, std::vector<double>(1));
	std::vector<std::vector<double>> test_labels(test_size, std::vector<double>(1));

	for(int i=0; i<test_size; ++i){
		double rand_x = (rand() % 10000)/5000.0 - 1;
		test_data[i][0] = rand_x;
		test_labels[i][0] = std::sin(rand_x);
	}		
	double prev_loss = nn.test(test_data, test_labels);
	std::cout << "initial_loss: " << prev_loss << std::endl;
	double loss = prev_loss;
	do{
		nn.train(train_data, train_labels);
		prev_loss = loss;
		loss = nn.test(test_data, test_labels);
		std::cout << "loss: " << loss << std::endl << std::endl;
	} while(prev_loss != loss);

	std::cout << "final loss: " << nn.test(test_data, test_labels) << std::endl << std::endl;

	std::ofstream ofs("nn_sin.txt");
	for(int i=0; i<100000; ++i){
		double rand_x = (rand() % 10000)/5000.0 - 1;
		std::vector<double> rand_i(1, rand_x);
		ofs << rand_x << " " << nn.predict(rand_i)[0] << std::endl;
	}
}

