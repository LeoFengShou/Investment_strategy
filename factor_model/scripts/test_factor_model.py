import unittest
import factor_model
from scipy.stats.mstats import gmean


class Test_Factor_Model(unittest.TestCase):

	def test_get_expected_factor_return(self):
		test_factor_returns = [[0.01, 0.02, 0.03], [0.02, -0.05, 0.08], [0.07, 0.05, 0.03], [0.02, 0.01, -0.09]]
		expected_factor_returns = factor_model.get_expected_factor_return(test_factor_returns)
		self.assertEqual(expected_factor_returns, [gmean([1.01, 1.02, 1.07, 1.02]) - 1, gmean([1.02, 0.95, 1.05, 1.01]) - 1, \
													gmean([1.03, 1.08, 1.03, 0.91]) - 1])



if __name__ == '__main__':
	unittest.main()