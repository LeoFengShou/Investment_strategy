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


INITIAL_PORFOLIO_VALUE = 1000 # This value in general doesn't matter, just for practical purposes


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--asset_data", default = "asset_data.json")
	parser.add_argument("--function", default = "Back-testing", help = "One of Back-testing" \
										+ ", Portfolio-domi, and Portfolio Construction")
	parser.add_argument("--user_input", default = "user_input.json", help = "The json file defines the user"\
										+ " input")
	args = parser.parse_args()
	with open(args.asset_data) as asset_data_in:
		asset_data = json.load(asset_data_in)
	

def main_flow(asset_data, function, user_input):
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
		return back_testing_procedure(asset_data, user_input)
	if function == "Portfolio-domi":
		if not ("start_date" in user_input and "end_date" in user_input and "weight" in user_input):
			print "not sufficient information provided in the user input"
			return False
		return port_domi_procedure(asset_data, user_input)
	if function == "Portfolio-Construction":
		if not ("start_date" in user_input and "end_date" in user_input and "target_return" in user_input):
			print "not sufficient information provided in the user input"
			return False
		return port_cont_procedure(asset_data, user_input)


def back_testing_procedure(asset_data, user_input):
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
		print("Start or end date exceeding range")
		return False
	SP500_values = asset_data["SP500"]["price_his"][feasible_start_date_index: feasible_start_date_index]
	dates = asset_data["SP500"]["dates"][feasible_start_date_index: feasible_start_date_index]
	portfolio_values = [0] * len(dates)
	cur_returns = [0] * (len(dates) - 1)
	shares = {} # {asset_name: num_shares}
	cur_value = {} # daily value of the portfolio {asset_name: dollar_value}
	for i in range(dates):
		date = dates[i]
		for asset_name in user_input["weight"].keys():
			if asset_name not in cur_value:
				cur_value[asset_name] = INITIAL_PORFOLIO_VALUE * user_input["weight"][asset_name]
			if date in asset_data[asset_name]["dates"]:
				date_index = asset_data[asset_name]["dates"].index(date)
				if asset_name not in shares:
					shares[asset_name] = user_input["weight"][asset_name] * INITIAL_PORFOLIO_VALUE \
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
	stats["total_return"] = portfolio_values[-1] / portfolio_values[0] - 1
	stats["mean_return"] = numpy.mean(cur_returns)
	stats["volitility"] = numpy.std(cur_returns)
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
	limit, i = 5, 0
	while target_date not in asset_data[asset_name]["dates"]:
		if i >= limit: break
		i += 1
		target_date_obj = datetime.datetime.strptime(target_date, "%Y-%m-%d") + datetime.timedelta(days=increment)
		target_date = datetime.datetime.strftime(target_date_obj, "%Y-%m-%d")
	return asset_data[asset_name]["dates"].index(target_date) if i < limit else -1