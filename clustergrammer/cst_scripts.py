def main():

	# retrieve_data()

	# make_ccle_exp_clust()

	print('here')

# make multiple CCLE NSCLC expression clustergrams 
# at different zscore cutoffs 
def make_ccle_exp_clust():
	from pymongo import MongoClient

	client = MongoClient()
	db = client.clustergrammer

	# load gene class information from harmonogram 
	gc = db.cst_data.find_one({'name':'gene_classes'})

	# define cutoffs
	z_cutoffs = [ 3, 3.5, 4 ]

	# define protein types 
	prot_types = ['KIN','PP','ACT','DACT','MET','DMET','TF', 'GPCR', 'IC', 'all']

	# load ccle data 
	ccle = db.cst_data.find_one({'name':'nsclc_allzc'})

	ccle = ccle['data']

	# minimum number intersect
	min_num_compare = 3
	# compare cutoff - the minimum absolute value that will be compared
	compare_cutoff = 0.1

	# loop through zscore cutoffs
	for inst_z in z_cutoffs:
		# loop through protein types 
		for inst_type in prot_types:
			
			print( '\n\n' + inst_type + '\t' + str(inst_z) + '\n')

			# cluster and output json
			export_dict = cluster_zscore( ccle, inst_type, inst_z, compare_cutoff, min_num_compare)

			# save to mongodb 
			db.cst_viz.insert( export_dict )

	client.close()

def cluster_zscore( ccle, inst_type, z_cutoff, compare_cutoff, min_num_compare ):
	import json_scripts
	import numpy as np
	from d3_clustergram_class import Network 

	net = Network()

	# # load ccle data with zscore normalization
	# ccle = json_scripts.load_to_dict('CCLE/nsclc_allzc.json')

	# convert zscored data to nparray 
	ccle['data_z'] = np.asarray(ccle['data_z'], dtype = float)

	# load gs_list to filter for kinase, tf etc
	# gs_list = json_scripts.load_to_dict('enz_and_tf_lists_gmts/categories_gs_list.json')
	gs_list = json_scripts.load_to_dict('gene_classes_harmonogram.json')

	# generate node lists 
	nodes = {}
	# get all genes 
	nodes['row'] = filter_genes_ccle(ccle, gs_list, inst_type, z_cutoff)
	# get all cell lines from CCLE 
	nodes['col'] = ccle['cell_lines']

	net.dat['nodes'] = nodes

	export_dict = {}

	# only make clustergram if there are genes remaining after filtering 
	# the minimum needed to produce a clustergram 
	if len(nodes['row']) > 1:

		print('there are ' + str(len(nodes['row'])) + ' genes being clustered' )

		# Generate data_mat: used to filter data from the original ccle for a subset of genes 
		# takes inputs: node lists for rows and columns, and primary data that will be used to make the matrix
		# the last two arguments are the names of the rows and columns in the original data
		data_mat = mat_from_ccle( nodes, ccle, 'gene', 'cell_lines', 'data_z' )

		net.dat['mat'] = data_mat

		net.cluster_row_and_col('cos')

		export_dict = {}
		export_dict['name'] = inst_type + '_' + str(z_cutoff)
		export_dict['z_cutoff'] = z_cutoff
		export_dict['dat'] = net.export_net_json('dat')
		export_dict['viz'] = net.export_net_json('viz')

	return export_dict

# gather all genes and cell lines 
def filter_genes_ccle(ccle, gs_list, inst_type, z_cutoff):
	import numpy as np 

	# get all gene names 
	all_genes = ccle['gene']

	# define the list of all genes as all the genes in ccle
	gs_list['all'] = all_genes 

	# filter for zscore here 
	#########################
	filtered_genes = []

	# loop through the genes and check if they are part of the gene class of interest 
	for inst_gene in all_genes:

		# check if gene of the type of interest 
		if inst_gene in gs_list[inst_type]:
			
			# get index of gene 
			inst_index =  all_genes.index(inst_gene)

			# get all zscores 
			inst_zscores = ccle['data_z'][inst_index,:]

			# get maximum zscore
			inst_max_z = np.amax(np.absolute(inst_zscores)) 

			# check if gene has zscore above cutoff 
			if inst_max_z > z_cutoff:
				filtered_genes.append(inst_gene)

	return filtered_genes

def mat_from_ccle( nodes, primary_data, row_name, col_name, data_name ):
    import scipy

    # print(primary_data.keys())

    # initialize data_mat 
    data_mat = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])

    # loop through rows
    for i in range(len(nodes['row'])):
      # loop through cols
      for j in range(len(nodes['col'])):

        # get inst_row and inst_col
        inst_row = nodes['row'][i]
        inst_col = nodes['col'][j]

        # find gene and cl index in zscored data 
        index_x = primary_data[row_name].index(inst_row)
        index_y = primary_data[col_name].index(inst_col)

        # map primary data to data_mat
        data_mat[i,j] = primary_data[data_name][ index_x, index_y ]

    # return data matrix 
    return data_mat 

def retrieve_data():
	from pymongo import MongoClient
	from d3_clustergram_class import Network

	client = MongoClient()

	# I only expect to find one document so I will use
	# find_one, which directly returns the document
	db = client.clustergrammer
	ptm = db.cst_data.find_one({'name':'prot_31_antimerge'})

	# print(ptm['data'].keys())

	net = Network()

	net.set_node_names('gene','cell_line')

	# load data to net.dat 
	net.load_data_to_net(ptm['data']['phos'])

	net.swap_nan_for_zero()
	cutoff_meet = 6
	min_num_meet = 4
	net.filter_network_thresh(cutoff_meet,min_num_meet)

	net.cluster_row_and_col('cos')

	# save the visualization 

	export_dict = {}
	export_dict['name'] = 'phos_ptm'
	export_dict['dat'] = net.export_net_json('dat')
	export_dict['viz'] = net.export_net_json('viz')

	# save to database 
	# tmp = db.cst_viz.find_one({'name':'phos_ptm'})

	db.cst_viz.remove({'name':'phos_ptm'})

	db.cst_viz.insert( export_dict )

	client.close()

main()