import unittest
import MVO


class Test_Factor_Model(unittest.TestCase):

	def test_get_weight_from_MVO(self):
		mu = [0.02, 0.1]
		Q = [[0.18,0.0021],[0.0022,0.09]]
		target_return = 0.07
		weight = MVO.get_weight_from_MVO(mu, Q, target_return)
		expected_weight = [0.3306, 0.6694]
		self.assertEqual(len(weight), len(expected_weight))
		for i in range(len(weight)):
			self.assertEqual(round(weight[i], 4), expected_weight[i])


if __name__ == '__main__':
	unittest.main()