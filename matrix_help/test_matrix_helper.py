import unittest
import matrix_helper


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


if __name__ == '__main__':
	unittest.main()