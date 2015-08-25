def main():

	# make expression clustergrams 
	make_expression_clustergrams()

	# return d3_json

# make tf-sub clustergram 
def tf_clust(tf_name):
	import json_scripts
	import d3_clustergram
	import numpy as np

	# load gs_list to filter genes by type 
	gs_list = json_scripts.load_to_dict('grammer/gene_classes_harmonogram.json')

	# load ccle data with zscore normalization
	ccle = json_scripts.load_to_dict('grammer/CCLE/nsclc_allzc.json')

	# convert zscored data to nparray 
	ccle['data_z'] = np.asarray(ccle['data_z'], dtype = float)

	print(len(ccle['gene']))

	# load tf downstream gene data 
	tf_union = json_scripts.load_to_dict('grammer/enz_and_tf_lists_gmts/TF/tf_union.json')

	print(type(tf_name))

	# find genes that are known to be targeted by transcription factor 
	target_genes = tf_union[tf_name]

	# add tf to list 
	target_genes.extend(tf_name)

	# get unique list of genes 
	target_genes = list(set(target_genes))

	print('there are ' + str(len(target_genes)) + ' genes targeted by ' + str(tf_name))

	# only keep targets that are significantly diff expressed 
	diff_exp_genes = filter_genes(ccle,gs_list,'all',3)
	
	# only keep target genes that were measured in ccle 
	target_genes = list(set(target_genes).intersection(diff_exp_genes))

	print('there are ' + str(len(target_genes)) + ' genes targeted by ' + str(tf_name))


	# generate clustergram 
	#########################

	# generate node lists 
	nodes = {}
	# get all genes 
	nodes['row'] = target_genes
	# get all cell lines from CCLE 
	nodes['col'] = ccle['cell_lines']

	# minimum number intersect
	min_num_int = 3

	# # only make clustergram if there are genes remaining after filtering 
	# # the minimum needed to produce a clustergram 
	# if len(nodes['row']) > 1:

	# 	print('there are ' + str(len(nodes['row'])) + ' genes being clustered' )

	# 	# Generate data_mat: used to filter data from the original ccle for a subset of genes 
	# 	# takes inputs: node lists for rows and columns, and primary data that will be used to make the matrix
	# 	# the last two arguments are the names of the rows and columns in the original data
	# 	data_mat = d3_clustergram.generate_data_mat_array( nodes, ccle, 'gene', 'cell_lines', 'data_z' )

	# 	# cluster rows and columns 
	# 	clust_order = d3_clustergram.cluster_row_and_column( nodes, data_mat, 'cosine', min_num_int )

	# 	# # write the d3_clustergram 
	# 	# # base_path = '/Applications/XAMPP/xamppfiles/htdocs/cst_gram/networks/'
	# 	# base_path = 'static/networks/'
	# 	# full_path = base_path + inst_type + '_exp_std_' + str(z_cutoff) + '.json'

	# 	# # write the clustergram 
	# 	# d3_clustergram.write_json_single_value(nodes, clust_order, data_mat, full_path)


	# generate matrix of transcription factor expression and target gene expression 

	# cluster

	# return clustergram 

	return {'tmp':'something'}

# make multiple CCLE NSCLC expression clustergrams 
# at different zscore cutoffs 
def make_expression_clustergrams():
	import json_scripts
	import os

	print(os.getcwd())	

	# load gene class information from harmonogram 
	gc = json_scripts.load_to_dict('grammer/gene_classes_harmonogram.json')

	# print(gc.keys())

	# define cutoffs
	# z_cutoffs = [ 0, 2, 2.5, 3, 3.5, 4 ]
	z_cutoffs = [ 3, 3.5 ]

	# define protein types 
	# prot_types = ['kin','pp','act','dact','met','dmet','tf', 'all']
	prot_types = ['all']
	# prot_types = ['PP']
	# prot_types = gc.keys()

	# loop through zscore cutoffs
	for inst_z in z_cutoffs:
		# loop through protein types 
		for inst_type in prot_types:
			print( '\n\n' + inst_type + '\t' + str(inst_z) + '\n')
			# cluster and output json
			cluster_zscore(inst_type, inst_z)

def cluster_zscore( inst_type, z_cutoff ):
	import json_scripts
	import d3_clustergram
	import numpy as np

	# load ccle data with zscore normalization
	ccle = json_scripts.load_to_dict('CCLE/nsclc_allzc.json')
	# convert zscored data to nparray 
	ccle['data_z'] = np.asarray(ccle['data_z'], dtype = float)

	# load gs_list to filter for kinase, tf etc
	# gs_list = json_scripts.load_to_dict('enz_and_tf_lists_gmts/categories_gs_list.json')
	gs_list = json_scripts.load_to_dict('gene_classes_harmonogram.json')

	# generate node lists 
	nodes = {}
	# get all genes 
	nodes['row'] = filter_genes(ccle, gs_list, inst_type, z_cutoff)
	# get all cell lines from CCLE 
	nodes['col'] = ccle['cell_lines']

	# minimum number intersect
	min_num_int = 3

	# only make clustergram if there are genes remaining after filtering 
	# the minimum needed to produce a clustergram 
	if len(nodes['row']) > 1:
		# print(len(nodes['row']))

		print('there are ' + str(len(nodes['row'])) + ' genes being clustered' )

		# Generate data_mat: used to filter data from the original ccle for a subset of genes 
		# takes inputs: node lists for rows and columns, and primary data that will be used to make the matrix
		# the last two arguments are the names of the rows and columns in the original data
		data_mat = d3_clustergram.generate_data_mat_array( nodes, ccle, 'gene', 'cell_lines', 'data_z' )

		# cluster rows and columns 
		clust_order = d3_clustergram.cluster_row_and_column( nodes, data_mat, 'cosine', min_num_int )

		# write the d3_clustergram 
		# base_path = '/Applications/XAMPP/xamppfiles/htdocs/cst_gram/networks/'
		base_path = 'static/networks/'
		full_path = base_path + inst_type + '_exp_std_' + str(z_cutoff) + '.json'

		# write the clustergram 
		d3_clustergram.write_json_single_value(nodes, clust_order, data_mat, full_path)

# gather all genes and cell lines 
def filter_genes(ccle, gs_list, inst_type, z_cutoff):
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

def load_cell_lines():

	# load the cell lines 
	filename = 'cell_lines.txt'

	# load the cell lines 
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()

	# clean up stray elemnets 
	cell_lines = []
	for inst_line in lines:
		cell_lines.append(inst_line.strip())

	return cell_lines

# # do not run main automatically 
# ################################
# # run main
# main()