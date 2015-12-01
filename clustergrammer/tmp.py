def main():
	import StringIO
	import pandas as pd 

	f = open('from_excel.txt','r')

	tmp = f.read()

	f.close()

	print(tmp)

	buff = StringIO.StringIO(tmp)

	print(buff)

	df = pd.read_table(buff, index_col=0)

	print(df)


def load_buffer():
	import pandas as pd 
	import io
	import StringIO

	# get buffer of file 
	io_buff = io.open('from_excel.txt', mode='r', buffering=-1)

	print(io_buff)
	print(str(io_buff))

	new_buff = str(io_buff)

	# read buffer into pandas dataframe 
	# tmp = pd.read_table(new_buff, index_col=0)
	# print(tmp)

def make_mult_views():
	# import network class from Network.py
	from d3_clustergram import Network
	from copy import deepcopy

	# set up range as function of maximum value in matrix 
	all_filt = range(10)

	inst_meet = 1

	print('something')

	# calc mult_view net 
	net_view = deepcopy(Network())
	# net_view.load_tsv_to_net('txt/example_tsv_network.txt')
	net_view.pandas_load_tsv_to_net('txt/ccle_example.txt')
	net_view.cluster_row_and_col('cos')

	net_view.viz['views'] = []

	all_views = []

	for inst_filt in all_filt:

	  print('\ninst_filt\t'+str(inst_filt))

	  # load network from tsv file
	  ##############################
	  net = deepcopy(Network())

	  net.dat = deepcopy(net_view.dat)

	  net.filter_network_thresh(inst_filt,inst_meet)

	  mat_shape = net.dat['mat'].shape

	  try:
	    # cluster
	    #############
	    # only compare vectors with at least min_num_comp common data points
	    # with absolute values above cutoff_comp
	    net.cluster_row_and_col('cos')

	    # add view 
	    inst_view = {}
	    inst_view['filt'] = inst_filt
	    inst_view['num_meet'] = inst_meet
	    inst_view['nodes'] = {}
	    inst_view['nodes']['row_nodes'] = net.viz['row_nodes']
	    inst_view['nodes']['col_nodes'] = net.viz['col_nodes']

	    all_views.append(inst_view)

	  except:
	    print('\n\ndo not make clustergram\n\n')

	# add views to viz
	net_view.viz['views'] = all_views

	# export data visualization to file
	######################################
	net_view.write_json_to_file('viz', 'json/mult_view.json', 'indent')

main()