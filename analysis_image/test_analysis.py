# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import sys
sys.path.append('./data')
from data import img2numpy_arr, generate_patches

import argparse
import numpy as np
import tflearn as tl
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--t', action='store', dest='test_path', type=str, help='Test Data Path')
	parser.add_argument('--i', action='store', dest='image_count', type=str, help='Test Image Count')
	config = parser.parse_args()

	#Load Test data
	image_count = (config.image_count).split(",")
	image_count = (int(image_count[0]), int(image_count[1]))
	patch_count = 20
	X = generate_patches(img2numpy_arr(config.test_path), image_count, patch_count)

	# Building 'Complex ConvNet'
	tl.init_graph(num_cores=2, gpu_memory_fraction=0.2)
	network = input_data(shape=[None, 42, 42, 3], name='input')

	network = conv_2d(network, 16, 3, activation='relu')
	network = conv_2d(network, 16, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = conv_2d(network, 64, 3, activation='relu')
	network = conv_2d(network, 64, 3, activation='relu')
	network = max_pool_2d(network, 2, strides=2)

	network = fully_connected(network, 256, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 256, activation='relu')
	network = dropout(network, 0.5)
	network = fully_connected(network, 9, activation='softmax')

	network = regression(network, optimizer='adam',
						 loss='categorical_crossentropy',
						 learning_rate=0.0001, name='target')

	# Model
	model = tl.DNN(network)
	model.load('analysis_model-828900')
	pred_y = model.predict(X)
	print(pred_y)
