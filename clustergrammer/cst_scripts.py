def main():
	retrieve_data()

def retrieve_data():
	from pymongo import MongoClient
	from d3_clustergram_class import Network

	client = MongoClient()

	# I only expect to find one document so I will use
	# find_one, which directly returns the document
	db = client.clustergrammer
	ptm = db.cst.find_one({'name':'prot_31_antimerge'})
	client.close()

	print(ptm['data'].keys())

	net = Network()

	net.set_node_names('gene','cell_line')

	# load data to net.dat 
	net.load_data_to_net(ptm['data']['phos'])

	net.swap_nan_for_zero()
	cutoff_meet = 6
	min_num_meet = 4
	net.filter_network_thresh(cutoff_meet,min_num_meet)

	net.cluster_row_and_col('cos',1,1)

main()