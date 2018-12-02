#include "NN.h"

NN::NN(const std::vector<int>& layer_sizes){
	srand(std::time(NULL));
	this->num_layers = layer_sizes.size();

	this->layers.resize(this->num_layers);
	for(int l_i=0; l_i<layer_sizes.size(); ++l_i){
		int layer_size = layer_sizes[l_i];

		// Add bias node to all but ouput layer
		if(l_i != this->num_layers-1) layer_size++;

		this->layers[l_i].resize(layer_size);

		//set bias nodes
		if(l_i != this->num_layers-1) this->layers[l_i][0] = 1;
	}

	// Setup activation holder
	this->activations = this->layers;

	this->weights.resize(this->num_layers-1);
	for(int w_i = 0; w_i < this->weights.size(); ++w_i){

		int prev_layer_size = this->layers[w_i].size();

		// No weights to next layer bias node
		int current_layer_size = this->layers[w_i+1].size() - 1;

		// Random weight initializations
		weights[w_i].resize(prev_layer_size, std::vector<double>(current_layer_size));	
		for(int r = 0; r < prev_layer_size; ++r){
			for(int c=0; c<current_layer_size; ++c){
				weights[w_i][r][c] = ((std::rand() - std::rand())%100000)/100000000.0;
			}
		}
	}
}

void NN::print_weights(){
	for(int w = 0; w < this->weights.size(); ++w){
		for(int r = 0; r < this->weights[w].size(); ++r){
			for(int c=0; c < this->weights[w][r].size(); ++c){
				std::cout << this->weights[w][r][c] << " ";
			}
			std::cout << std::endl;
		}
	}
}

// Sigmoid activation function
double NN::activation(double x){
	return 1 / (1 + std::exp(-1 * x));
}

/// Sigmoid prime
double NN::activation_prime(double x){
	return activation(x) * (1 - activation(x));
};

std::vector<double> NN::feed_forward(const std::vector<double>& input){

	if(input.size() != this->layers[0].size()-1){
		std::cout << "Can't feedforward, input layer size of " << input.size() << " doesn't match expected " << this->layers[0].size()-1 << std::endl;
		return {};
	}

	// Set up input layer
	for(int i=0; i<input.size(); ++i){
		this->layers[0][i+1] = input[i];
		this->activations[0][i+1] = input[i];
	}

	// Propagate through middle layers
	for(int l_i=1; l_i<this->num_layers; ++l_i){
		int t_i = 1;
		if(l_i != this->num_layers-1) t_i = 0;
		for(; t_i<this->layers[l_i].size(); ++t_i){
			this->activations[l_i][t_i] = 0;
			for(int p_i=0; p_i<this->layers[l_i-1].size(); ++p_i){
				this->activations[l_i][t_i] += this->layers[l_i-1][p_i] * this->weights[l_i-1][p_i][t_i-1];
			}
			this->layers[l_i][t_i] = this->activation(this->activations[l_i][t_i]);
		}
	}

	//  Return output node values
	std::vector<double>& output_layer = this->layers[this->num_layers-1];
	return output_layer;
}

// Train using squared classification error loss function
double NN::train(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels){
	if(data.size() && data[0].size() != this->layers[0].size()-1){
		std::cout << "Input data wrong dimension!" << std::endl;	
		return -1;
	}
	if(labels.size() != data.size()){
		std::cout << "Input labels don't match data" << std::endl;
		return -1;
	}
	if(labels.size() && labels[0].size() != this->layers[this->num_layers-1].size()){
		std::cout << "Input labels don't match last nn layer!" << std::endl;
		return -1;
	}
	
	return 0;
}
