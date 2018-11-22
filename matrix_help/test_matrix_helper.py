import unittest
import matrix_helper
from numpy import dot, array


class Test_Factor_Model(unittest.TestCase):
	
	def test_add_to_each_row(self):
		test_matrix = [[1,2],[3,4]]
		matrix_helper.add_to_each_row(test_matrix, 1, 5)
		self.assertEqual(test_matrix, [[1,5,2],[3,5,4]])
		matrix_helper.add_to_each_row(test_matrix, 0, 5)
		self.assertEqual(test_matrix, [[5,1,5,2],[5,3,5,4]])
		matrix_helper.add_to_each_row(test_matrix, 4, 5)
		self.assertEqual(test_matrix, [[5,1,5,2],[5,3,5,4]])
		matrix_helper.add_to_each_row(test_matrix, 5, 5)
		self.assertEqual(test_matrix, [[5,1,5,2],[5,3,5,4]])
		matrix_helper.add_to_each_row(test_matrix, -1, 5)
		self.assertEqual(test_matrix, [[5,1,5,2],[5,3,5,4]])

	def test_add_to_each_ele(self):
		test_matrix = [[1,2],[3,4]]
		matrix_helper.add_to_each_ele(test_matrix, 2)
		self.assertEqual(test_matrix, [[3,4],[5,6]])

	def test_cvxopt_solve_qp(self):
		M = array([[1., 2., 0.], [-8., 3., 2.], [0., 1., 1.]])
		P = dot(M.T, M)
		q = dot(array([3., 2., 3.]), M).reshape((3,))
		G = array([[1., 2., 1.], [2., 0., 1.], [-1., 2., -1.]])
		h = array([3., 2., -2.]).reshape((3,))
		test_res = matrix_helper.cvxopt_solve_qp(P, q, G, h)
		excp_res = array([-0.49025721, -1.57755278, -0.66484775])
		self.assertEqual(len(test_res), len(excp_res))
		for i in range(len(excp_res)):
			self.assertEqual(round(test_res[i], 4), round(excp_res[i], 4))


if __name__ == '__main__':
	unittest.main()