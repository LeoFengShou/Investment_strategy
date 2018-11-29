'''
	Title: Main engine
	Author: Leo Feng
	Description: This is in charge of the main flow of the investment machine,
				 from reading data to calling each investment strategy to presenting result.
'''
import json
import argparse
import datetime
import numpy
import copy

import factor_model
import MVO
import cvar
import matrix_helper


INITIAL_PORFOLIO_VALUE = 1000 # This value in general doesn't matter, just for practical purposes
ORIGINAL_CONSTANT = 0.5 # The extent to which to keep the original portfolio
AMPLIFY_FACTOR = 1.5


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--asset_data", default = "asset_data.json")
	parser.add_argument("--function", default = "Back-testing", help = "One of Back-testing" \
										+ ", Portfolio-domi, and Portfolio Construction")
	parser.add_argument("--user_input", default = "user_input.json", help = "The json file defines the user"\
										+ " input")
	parser.add_argument("--id_ticker_mapping", default = "id_ticker_mapping.json")
	parser.add_argument("--ticker_id_mapping", default = "ticker_id_mapping.json")
	parser.add_argument("--factor_data", default = "factor_data.json")
	args = parser.parse_args()
	with open(args.asset_data, "r") as asset_data_in:
		asset_data = json.load(asset_data_in)
	with open(args.user_input, "r") as user_input_in:
		user_input = json.load(user_input_in)
	with open(args.id_ticker_mapping, "r") as id_ticker_mapping_in:
		id_ticker_mapping = json.load(id_ticker_mapping_in)
	with open(args.ticker_id_mapping, "r") as ticker_id_mapping_in:
		ticker_id_mapping = json.load(ticker_id_mapping_in)
	with open(args.factor_data, "r") as factor_data_in:
		factor_data = json.load(factor_data_in)
	# results1 = main_flow(asset_data, "Back-testing", user_input, id_ticker_mapping, ticker_id_mapping, factor_data)
	results2 = main_flow(asset_data, "Portfolio-domi", user_input, id_ticker_mapping, ticker_id_mapping, factor_data)
	import pdb; pdb.set_trace()
	

def main_flow(asset_data, function, user_input, id_ticker_mapping, ticker_id_mapping, factor_data):
	'''
		asset_data: the variable holding all the information about the assets
		function: one of Back-testing, Portfolio-domi, and Portfolio-Construction
		user_input: one example is listed as follows
			user_input = {
				weight: {
					asset_name: weight_percent
				}
				target_return: percent
				start_date: yyyy-mm-dd
				end_date: yyyy-mm-dd
			}
	'''
	if function == "Back-testing":
		if not ("start_date" in user_input and "end_date" in user_input and "weight" in user_input):
			print "not sufficient information provided in the user input"
			return False
		return back_testing_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping)
	if function == "Portfolio-domi":
		if not ("start_date" in user_input and "end_date" in user_input and "weight" in user_input):
			print "not sufficient information provided in the user input"
			return False
		return port_domi_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping, factor_data)
	if function == "Portfolio-Construction":
		if not ("start_date" in user_input and "end_date" in user_input and "target_return" in user_input):
			print "not sufficient information provided in the user input"
			return False
		return port_cont_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping)


def back_testing_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping):
	'''
		Input: 
			asset_data: the variable holding all the information about the assets
			user_input: the user input must contain start_date, end_date, and weight
		return:
			a tuple of three list:
				portfolio_values
				SP500_values
				dates
				stats
	'''
	feasible_start_date_index = find_next_available_date_index(asset_data, user_input["start_date"], "SP500", +1)
	feasible_end_date_index = find_next_available_date_index(asset_data, user_input["end_date"], "SP500", -1)
	if feasible_start_date_index == -1 or feasible_end_date_index == -1:
		import pdb; pdb.set_trace()
		print("Start or end date exceeding range")
		return False
	SP500_values = asset_data["SP500"]["price_his"][feasible_start_date_index: feasible_end_date_index + 1]
	dates = asset_data["SP500"]["dates"][feasible_start_date_index: feasible_end_date_index + 1]
	portfolio_values = [0] * len(dates)
	cur_returns = [0] * (len(dates) - 1)
	shares = {} # {asset_name: num_shares}
	cur_value = {} # daily value of the portfolio {asset_name: dollar_value}
	for i in range(len(dates)):
		date = dates[i]
		for ticker in user_input["weight"].keys():
			asset_name = ticker_id_mapping[ticker]
			# import pdb; pdb.set_trace()
			if asset_name not in cur_value:
				cur_value[asset_name] = INITIAL_PORFOLIO_VALUE * user_input["weight"][ticker]
			if date in asset_data[asset_name]["dates"]:
				date_index = asset_data[asset_name]["dates"].index(date)
				if asset_name not in shares:
					shares[asset_name] = user_input["weight"][ticker] * INITIAL_PORFOLIO_VALUE \
								/ asset_data[asset_name]["price_his"][date_index]
				cur_value[asset_name] = shares[asset_name] * \
									asset_data[asset_name]["price_his"][date_index]
		new_port_value = 0
		for asset_name in cur_value.keys():
			new_port_value += cur_value[asset_name]
		portfolio_values[i] = new_port_value
		if i > 0:
			cur_returns[i - 1] = portfolio_values[i] / portfolio_values[i - 1] - 1
	stats = {}
	# try:
	stats["total_return"] = portfolio_values[-1] / portfolio_values[0] - 1
	# except:
		# import pdb; pdb.set_trace()
	stats["mean_return"] = numpy.mean(cur_returns)
	stats["volitility"] = numpy.std(cur_returns) / (len(cur_returns) ** 0.5)
	stats["sharpe"] = stats["mean_return"] / stats["volitility"]
	return {"portfolio_values": portfolio_values, "SP500_values": SP500_values, "dates": dates, "stats": stats}


def find_next_available_date_index(asset_data, target_date, asset_name, increment):
	'''
		Description: Find the first available date near the target_date according to increment
		Input:
			asset_data: same as above
			asset_name: the ticker of the asset, such as AAPL
			target_date: the date whose index is desired
			increment: either +1 for starting date or -1 for ending date
		Return:
			The index of the available date in the -asset_data[asset_name]["dates"]
			if not found, return -1
	'''
	limit, i = 32, 0
	while target_date not in asset_data[asset_name]["dates"]:
		if i >= limit: break
		i += 1
		target_date_obj = datetime.datetime.strptime(target_date, "%Y-%m-%d") + datetime.timedelta(days=increment)
		target_date = datetime.datetime.strftime(target_date_obj, "%Y-%m-%d")
	return asset_data[asset_name]["dates"].index(target_date) if i < limit else -1


def port_domi_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping, factor_data):
	original_user_input = copy.deepcopy(user_input)
	if user_input["start_date"] < "2004-01-31": user_input["start_date"] = "2004-01-31"
	if user_input["end_date"] > "2018-10-31": user_input["end_date"] = "2018-10-31"
	# print "call here -1"
	user_port_res_whole = back_testing_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping)
	feasible_start_date_index = find_next_available_date_index(asset_data, user_input["start_date"], "SP500", +1)
	feasible_end_date_index = find_next_available_date_index(asset_data, user_input["end_date"], "SP500", -1)
	dates = asset_data["SP500"]["dates"][feasible_start_date_index: feasible_end_date_index + 1]
	# rebalance_dates = [0] * 10
	# for i in range(10):
	# 	rebalance_dates[i] = dates[i * int(len(dates) / 10)]
	# rebalance_dates = sorted(list(set(rebalance_dates)))
	dates = asset_data["SP500"]["dates"][feasible_start_date_index - 48: feasible_start_date_index] + dates
	# cur_portfolio = {} # {asset_name: weight(decimal)}
	# for ticker in user_input["weight"]:
	# 	asset_name = ticker_id_mapping[ticker]
	# 	cur_portfolio[asset_name] = user_input["weight"][ticker] * ORIGINAL_CONSTANT
	portfolio_values = [INITIAL_PORFOLIO_VALUE]
	cur_portfolio = {}
	cur_returns = []
	start_debug = False
	for i in range(48, len(dates), 1):
		date = dates[i]
		user_input["start_date"] = dates[i - 48]  # Look back 4 years each time
		user_input["end_date"] = date
		# print "call here", i
		# try:
		user_port_res = back_testing_procedure(asset_data, user_input, id_ticker_mapping, ticker_id_mapping)
		# except:
			# import pdb; pdb.set_trace()
		factor_matrix = prepare_factor_matrix(factor_data, i - 48, i, dates)
		assets_included, asset_return_matrix = prepare_asset_return_matrix(asset_data, \
												user_input["start_date"], user_input["end_date"], dates)
		expected_returns, covariance_matrix = factor_model.generate_factor(factor_matrix, asset_return_matrix)
		weight = MVO.get_weight_from_MVO(expected_returns, covariance_matrix, \
											user_port_res["stats"]["mean_return"] * AMPLIFY_FACTOR)
		new_port_value = 0
		for asset_name in cur_portfolio.keys():
			if date in asset_data[asset_name]["dates"]:
				new_port_value += asset_data[asset_name]["price_his"][asset_data[asset_name]["dates"].index(date)] \
								* cur_shares[asset_name]
				print new_port_value, asset_data[asset_name]["price_his"][asset_data[asset_name]["dates"].index(date)], cur_shares[asset_name]
			else:
				new_port_value += portfolio_values[-1] * cur_portfolio[asset_name]
				print portfolio_values[-1], cur_portfolio[asset_name]
				print "here"
			# import pdb; pdb.set_trace()
		if new_port_value != 0:
			portfolio_values.append(new_port_value)
			print new_port_value
		else:
			if new_port_value < 0:
				import pdb; pdb.set_trace()
		cur_portfolio = {} # {asset_name: weight(decimal)}
		for ticker in user_input["weight"]:
			asset_name = ticker_id_mapping[ticker]
			cur_portfolio[asset_name] = user_input["weight"][ticker] * ORIGINAL_CONSTANT
		for j2 in range(len(weight)):
			if assets_included[j2] in cur_portfolio:
				cur_portfolio[assets_included[j2]] += weight[j2] * (1 - ORIGINAL_CONSTANT)
			else:
				cur_portfolio[assets_included[j2]] = weight[j2] * (1 - ORIGINAL_CONSTANT)
		su = 0
		for wei in cur_portfolio.keys():
			su += cur_portfolio[wei] 
		if su > 1.01:
			import pdb; pdb.set_trace()
		print weight
		cur_shares = {} # {asset_name: #shares}
		for asset_name in cur_portfolio.keys():
			# try:
			if date in asset_data[asset_name]["dates"]:
					cur_shares[asset_name] = portfolio_values[-1] * cur_portfolio[asset_name] / \
								asset_data[asset_name]["price_his"][asset_data[asset_name]["dates"].index(date)]
			# except:
				# import pdb; pdb.set_trace()
		# import pdb; pdb.set_trace()
		# print new_port_value 
		# print cur_portfolio
		# print cur_shares
		# print 
		if len(portfolio_values) > 1:
			cur_returns.append(portfolio_values[-1] / portfolio_values[-2] - 1)
	stats = {}
	stats["total_return"] = portfolio_values[-1] / portfolio_values[0] - 1
	stats["mean_return"] = numpy.mean(cur_returns)
	stats["volitility"] = numpy.std(cur_returns) / (len(cur_returns) ** 0.5)
	stats["sharpe"] = stats["mean_return"] / stats["volitility"]
	return {	"original_value": {"portfolio_values": user_port_res_whole["portfolio_values"], \
									"stats": user_port_res_whole["stats"]}, \
				"dominant": {"portfolio_values": portfolio_values, "stats": stats}, \
				"dates": user_port_res_whole["dates"]}


def prepare_factor_matrix(factor_data, start_date_i, end_date_i, dates):
	factor_matrix = []
	for i in range(start_date_i + 1, end_date_i + 1):
		factor_matrix.append(factor_data[dates[i][:7].replace("-", "")])
	return factor_matrix


def prepare_asset_return_matrix(asset_data, start_date, end_date, dates):
	assets_included = [] # [asset_name] that are included in the matrix, only when both start and end date are 
						# available, the asset will be included
	asset_return_matrix = []
	for asset_name in asset_data.keys():
		if start_date in asset_data[asset_name]["dates"] and end_date in asset_data[asset_name]["dates"]:
			asset_return_matrix.append(asset_data[asset_name]["ret_his"]\
									[asset_data[asset_name]["dates"].index(start_date) + 1: \
									 asset_data[asset_name]["dates"].index(end_date) + 1])
			if len(asset_data[asset_name]["ret_his"]\
									[asset_data[asset_name]["dates"].index(start_date) + 1: \
									 asset_data[asset_name]["dates"].index(end_date) + 1]) != 48:
				import pdb; pdb.set_trace()
			assets_included.append(asset_name)
	return assets_included, matrix_helper.transpose(asset_return_matrix)


if __name__ == '__main__':
	main()