#include "NN.h"
#include "MatrixUtil.h"

NN::NN(const std::vector<int>& layer_sizes){
	srand(std::time(NULL));
	this->num_layers = layer_sizes.size();

	this->layers.resize(this->num_layers);
	for(int l_i=0; l_i<this->num_layers; ++l_i){
		int layer_size = layer_sizes[l_i];

		// Add bias node to all but ouput layer
		if(l_i != this->num_layers-1) layer_size++;

		this->layers[l_i] = std::vector<double>(layer_size, 0);

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
		if(w_i == this->weights.size()-1) current_layer_size++;

		// Random weight initializations
		weights[w_i].resize(prev_layer_size, std::vector<double>(current_layer_size));	
		for(int r = 0; r < prev_layer_size; ++r){
			for(int c=0; c<current_layer_size; ++c){
				weights[w_i][r][c] = ((std::rand() - std::rand())%100000)/1000000.0;
			}
		}
	}

	this->best_loss = (1<<30);
	this->best_weights = this->weights;
}

void NN::print_weights(){
	for(int i=0; i<this->weights.size(); ++i) print_matrix(this->weights[i]);
}

// Sigmoid activation function
double NN::activation(double x){
	return 1 / (1 + std::exp(-1 * x));
}

/// Sigmoid prime
double NN::activation_prime(double x){
	return activation(x) * (1 - activation(x));
};

std::vector<double>& NN::feed_forward(const std::vector<double>& input){

	if(input.size() != this->layers[0].size()-1){
		std::cout << "Can't feedforward, input layer size of " << input.size() << " doesn't match expected " << this->layers[0].size()-1 << std::endl;
		return this->layers[this->num_layers-1];
	}

	// Set up input layer
	for(int i=0; i<input.size(); ++i){
		this->layers[0][i+1] = activation(input[i]);
		this->activations[0][i+1] = input[i];
	}

	// Propagate through middle layers
	for(int l_i=1; l_i<this->num_layers; ++l_i){
		int current_layer_i = l_i == this->num_layers-1 ? 0 : 1;
		if(this->layers[l_i-1].size() != this->weights[l_i-1].size()) throw -1;
		for(int weight_index=0; weight_index < this->weights[l_i-1][0].size(); ++weight_index, ++current_layer_i){
			this->activations[l_i][current_layer_i] = 0;
			for(int p_i=0; p_i<this->layers[l_i-1].size(); ++p_i){
				this->activations[l_i][current_layer_i] += this->layers[l_i-1][p_i] * this->weights[l_i-1][p_i][weight_index];
			}
			this->layers[l_i][current_layer_i] = this->activation(this->activations[l_i][current_layer_i]);
		}
	}

	//  Return output node values
	std::vector<double>& output_layer = this->layers[this->num_layers-1];
	return output_layer;
}

// Train using squared classification error loss function
void NN::train(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels){
	if(data.size() && data[0].size() != this->layers[0].size()-1){
		std::cout << "Input data wrong dimension!" << std::endl;	
		return;
	}
	if(labels.size() != data.size()){
		std::cout << "Input labels don't match data" << std::endl;
		return;
	}
	if(labels.size() && labels[0].size() != this->layers[this->num_layers-1].size()){
		std::cout << "Input labels don't match last nn layer!" << std::endl;
		return;
	}
	for(int data_i=0; data_i<data.size(); ++data_i){
		std::vector<double> loss_prime = this->feed_forward(data[data_i]);

		for(int i=0; i<loss_prime.size(); ++i){
			loss_prime[i] -= labels[data_i][i];
		}

		// Backprop

		std::vector<std::vector<double>> current(1);
		current[0] = loss_prime;

		for(int w_i = this->weights.size()-1; w_i >= 0; --w_i){
			int layer_i = w_i+1;

			int activation_count = this->activations[layer_i].size();
			// Don't include bias nodes
			if(w_i != this->weights.size()-1) activation_count--;
			
			std::vector<std::vector<double>> activation_primes(activation_count, std::vector<double>(activation_count, 0));

			int node_i = 0;
			// Don't include bias node
			if(w_i != this->weights.size()-1) node_i++;
			for(int i=0; i<activation_count; ++i) activation_primes[i][i] = this->activation_prime(this->activations[layer_i][node_i++]);

			current = matrix_mult(current, activation_primes);

			// Get transpose of current weights (exluding bias node);
			std::vector<std::vector<double>> weights_t(this->weights[w_i].size()-1, std::vector<double>(this->weights[w_i][0].size()));
			for(int i=0; i<weights_t.size(); ++i){
				for(int j=0; j<weights_t[0].size(); ++j){
					weights_t[i][j] = this->weights[w_i][i+1][j];
				}
			}
			weights_t = matrix_transpose(weights_t);

			// adjust bias weights
			for(int i=0; i<this->weights[w_i].size(); ++i) this->weights[w_i][0][i] -= this->learning_rate * current[0][i];

			// adjust weights from layer
			for(int i=1; i<this->weights[w_i].size(); ++i){
				for(int j=0; j<this->weights[w_i][0].size(); ++j){
					this->weights[w_i][i][j] += this->learning_rate * current[0][j] * this->activations[layer_i-1][i];
				}
			}

			// Propagate error to next (previous) layer	
			current = matrix_mult(current, weights_t);
		}
	}
}

std::vector<std::vector<double>> NN::predict(const std::vector<std::vector<double>>& input){
	std::vector<std::vector<double>> result(input.size());
	for(int i=0; i<input.size(); ++i){
		result[i] = this->feed_forward(input[i]);	
	}
	return result;
}

std::vector<double> NN::predict(const std::vector<double>& input){
	std::vector<std::vector<double>> input_t(1, input);
	return this->predict(input_t)[0];
}

double NN::test(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels){
	double loss = 0;
	std::vector<std::vector<double>> guesses = this->predict(data);
	for(int i=0; i<guesses.size(); ++i){
		for(int j=0; j<guesses[i].size(); ++j){
			double err = (guesses[i][j] - labels[i][j]);
			loss += err * err;
			if(isnan(loss)){
				std::cout << "NANANANAANNA: " << err << std::endl;
				throw -1;
			}
		}
	}
	if(loss < best_loss) this->best_weights = this->weights;
	return loss;
}
