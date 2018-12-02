#ifndef __NN_H_
#define __NN_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fstream>

#include <cmath>

#include <vector>
#include <iostream>

class NN {

	private:

		int num_layers;
		std::vector<std::vector<std::vector<double>>> weights;
		std::vector<std::vector<double>> layers;
		std::vector<std::vector<double>> activations;

		double learning_rate = 0.01;

		std::vector<double>& feed_forward(const std::vector<double>& input);
		double activation(double x);
		double activation_prime(double x);

	public:	

		NN(const std::vector<int>& layer_sizes);

		void train(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels);
		double test(const std::vector<std::vector<double>>& data, const std::vector<std::vector<double>>& labels);
		std::vector<std::vector<double>> predict(const std::vector<std::vector<double>>& input);
		std::vector<double> predict(const std::vector<double>& input);
		void print_weights();
};

#endif
