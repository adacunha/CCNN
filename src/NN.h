#ifndef __NN_H_
#define __NN_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <cmath>

#include <vector>
#include <iostream>

class NN {

	private:

		int num_layers;
		std::vector<std::vector<std::vector<double>>> weights;
		std::vector<std::vector<double>> layers;
		std::vector<std::vector<double>> activations;

		double learning_rate = .01;

		std::vector<double>& feed_forward(const std::vector<double>& input);
		double activation(double x);
		double activation_prime(double x);

	public:	

		NN(const std::vector<int>& layer_sizes);

		double train(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels);
		void print_weights();
};

#endif
