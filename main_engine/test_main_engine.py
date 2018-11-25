'''
	Author: Leo Feng
'''

import unittest
import main_engine
from numpy import dot, array


class TestMainEngine(unittest.TestCase):
	
	def test_find_next_available_date_index(self):
		asset_data = {"SP500": {"dates": ["2008-08-08"]}}
		target_date = "2008-08-08"
		asset_name = "SP500"
		increment = 1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 0)

		asset_data = {"SP500": {"dates": ["2008-08-08", "2008-08-09", "2008-08-10", "2008-08-11",\
											"2008-08-14", "2008-08-15", "2008-08-16", "2008-08-17",\
											"2008-08-21", "2008-08-22", "2008-08-25"]}}
		target_date = "2008-08-11"
		asset_name = "SP500"
		increment = 1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 3)

		target_date = "2008-08-25"
		asset_name = "SP500"
		increment = 1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 10)

		target_date = "2008-08-12"
		asset_name = "SP500"
		increment = 1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 4)

		target_date = "2008-08-26"
		asset_name = "SP500"
		increment = 1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, -1)

		target_date = "2008-08-26"
		asset_name = "SP500"
		increment = -1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 10)

		target_date = "2008-08-08"
		asset_name = "SP500"
		increment = -1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, 0)

		target_date = "2008-08-07"
		asset_name = "SP500"
		increment = -1 # for starting date
		date_index = main_engine.find_next_available_date_index(asset_data, target_date, asset_name, increment)
		self.assertEqual(date_index, -1)
		

if __name__ == '__main__':
	unittest.main()