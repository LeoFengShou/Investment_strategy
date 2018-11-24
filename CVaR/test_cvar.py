'''
	Author: Leo Feng
'''

import unittest
import cvar


class Test_Factor_Model(unittest.TestCase):
	
	def test_get_optimal_weight_by_CVaR(self):
		mu = [0.02, 0.1]
		Q = [[0.18,0.0022],[0.0022,0.09]]
		cur_p = [1, 2]
		weight = cvar.get_optimal_weight_by_CVaR(mu, Q, cur_p)
		print weight


if __name__ == '__main__':
	unittest.main()