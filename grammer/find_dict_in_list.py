# find a dict in a list of dicts by searching for a value 
def main(list_dict, search_value, search_string):

	# get all the possible values of search_value
	all_values = [d[search_value] for d in list_dict]

	# check if the search value is in the keys 
	if search_string in all_values:
		# find the dict 
		found_dict = (item for item in list_dict if item[search_value] == search_string).next()
	else:
		found_dict = {}

	# return the found dictionary
	return found_dict