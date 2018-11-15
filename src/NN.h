#ifndef __NN_H_
#define __NN_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>


class NN {
	private:
		int num_layers;
		std::vector<std::vector<std::vector<double>>> weights;
		std::vector<std::vector<double>> layers;
	public:	
		NN(std::vector<int> layer_sizes){
			this->num_layers = layer_sizes.size();

			this->layers.resize(this->num_layers);
			for(int l_i=0; l_i<layer_sizes.size(); ++l_i){
				srand(std::time(NULL));
				int layer_size = layer_sizes[l_i];

				// Add bias node
				layer_size++;
				this->layers[l_i].resize(layer_size);

				//set bias nodes
				this->layers[l_i][0] = 1;
			}

			this->weights.resize(num_layers-1);
			for(int w_i = 0; w_i < this->weights.size(); ++w_i){

				int prev_layer_size = this->layers[w_i].size();

				int current_layer_size = this->layers[w_i+1].size();
				current_layer_size--;

				weights[w_i].resize(prev_layer_size, std::vector<double>(current_layer_size));	
				for(int r = 0; r < prev_layer_size; ++r){
					for(int c=0; c<current_layer_size; ++c){
						weights[w_i][r][c] = ((std::rand() - std::rand())%100000)/100000000.0;
					}
				}
			}
		}

		void print_weights(){
			for(int w = 0; w < this->weights.size(); ++w){
				for(int r = 0; r < this->weights[w].size(); ++r){
					for(int c=0; c < this->weights[w][r].size(); ++c){
						std::cout << this->weights[w][r][c] << " ";
					}
					std::cout << std::endl;
				}
			}
		}

		std::vector<double> feed_forward(std::vector<double> input){
			if(input.size() != this->layers[0].size()-1){
				std::cout << "Can't feedforward, input layer size of " << input.size() << " doesn't match expected " << this->layers[0].size()-1 << std::endl;
				return {};
			}
			// Set up input layer
			for(int i=0; i<input.size(); ++i){
				this->layers[0][i+1] = input[i];
			}

			// Propagate through middle layers
			for(int l_i=1; l_i<this->num_layers; ++l_i){
				for(int t_i=1; t_i<this->layers[l_i].size(); ++t_i){
					this->layers[l_i][t_i] = 0;
					for(int p_i=0; p_i<this->layers[l_i-1].size(); ++p_i){
						this->layers[l_i][t_i] += this->layers[l_i-1][p_i] * this->weights[l_i-1][p_i][t_i-1];
					}
				}
			}
			std::vector<double>& output_layer = this->layers[this->layers.size()-1];
			return std::vector<double>(output_layer.begin()+1, output_layer.end());
		}
};

#endif
