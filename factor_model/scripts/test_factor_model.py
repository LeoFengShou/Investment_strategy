import unittest
import factor_model
from scipy.stats.mstats import gmean


class Test_Factor_Model(unittest.TestCase):

	def test_get_expected_factor_return(self):
		test_factor_returns = [[0.01, 0.02, 0.03], [0.02, -0.05, 0.08], [0.07, 0.05, 0.03], [0.02, 0.01, -0.09]]
		expected_factor_returns = factor_model.get_expected_factor_return(test_factor_returns)
		self.assertEqual(expected_factor_returns, [gmean([1.01, 1.02, 1.07, 1.02]) - 1, gmean([1.02, 0.95, 1.05, 1.01]) - 1, \
													gmean([1.03, 1.08, 1.03, 0.91]) - 1])


	def test_generate_factor(self):
		test_factor_returns = [	[0.01, 0.02, 0.03], \
								[0.02, -0.05, 0.08], \
								[0.07, 0.05, 0.03], \
								[0.02, 0.01, -0.09]]
								# Three factors' history in 4-day period

		test_asset_returns = [	[0.04, 0.06], \
								[0.03, -0.02], \
								[0.01, 0.04], \
								[0.04, 0.02]]

		expected_returns = [0.0302, 0.0242]

		test_expected_returns, test_covariance_matrix = factor_model.generate_factor(test_factor_returns, test_asset_returns)
		
		for i in range(len(test_expected_returns)):
			self.assertEqual(expected_returns[i], round(test_expected_returns[i], 4))

		expected_covariance_matrix = [[0.0002, 0.0], [0.0, 0.0012]]
		for i in range(len(expected_covariance_matrix)):
			for j in range(len(expected_covariance_matrix[0])):
					self.assertEqual(expected_covariance_matrix[i][j], round(test_covariance_matrix[i][j], 4))


if __name__ == '__main__':
	unittest.main()