import numpy as np 
from numpy.linalg import inv
from numpy import matmul



def add_to_each_row(matrix, index, to_add):
	'''
		For each row of matrix, add to_add to the position of index and shift the rest.

		Example:
			add_to_each_row([[1,2],[3,4]], 1, 5) returns [[1,5,2],[3,5,4]]
	'''
	for i in range(len(matrix)):
		if index >= len(matrix[0]) or index < 0:
			return
		matrix[i] = matrix[i][:index] + [to_add] + matrix[i][index:]


def add_to_each_ele(matrix, to_add):
	'''
		Add to_add to each element of the matrix
	'''
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			matrix[i][j] += to_add