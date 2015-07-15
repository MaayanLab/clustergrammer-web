def main( gmt_colors, inst_genes, num_terms, dist_type):

	print('in main function of make_enr_clust')
  
	# get list of gmts
	gmt_names = gmt_colors.keys()

	print(gmt_colors)

	print('\ngmt colors '+ gmt_names[0] + '\n')

	# make the post request with the input genes 
	# and get the userListId that will be used later for referencing the list 
	userListId = enrichr_post_request(inst_genes, '')

	# initialize enr
	enr = []

	# loop through gmts 
	for inst_gmt in gmt_colors:

		# get results from enrichr
		# return a list of dictionaries 
		inst_enr = enrichr_get_request(inst_gmt, num_terms, userListId, gmt_colors[inst_gmt] )

		if len(enr) == 0:
			enr = inst_enr 
		else:
			enr.extend(inst_enr)

	# make clustergram 
	d3_json = make_enrichment_clustergram(enr, dist_type)

	return d3_json

# make clustergram
def make_enrichment_clustergram(enr, dist_type):
	import d3_clustergram

	# make a dictionary of enr_terms and colors 
	terms_colors = {}
	for inst_enr in enr:
		terms_colors[inst_enr['name']] = inst_enr['color']

	# print(terms_colors)

	# convert enr to nodes, data_mat 
	nodes, data_mat = d3_clustergram.convert_enr_to_nodes_mat( enr )

	# cluster rows and columns 
	clust_order = d3_clustergram.cluster_row_and_column( nodes, data_mat, dist_type, enr )

	# generate d3_clust json 
	d3_json = d3_clustergram.d3_clust_single_value( nodes, clust_order, data_mat, terms_colors )

	return d3_json

# make the get request to enrichr using the requests library 
# this is done before making the get request with the gmt name 
def enrichr_post_request( input_genes, meta=''):
  # get metadata 
	import requests
	import json

	# stringify list 
	input_genes = '\n'.join(input_genes)

	# define post url 
	post_url = 'http://amp.pharm.mssm.edu/Enrichr/addList'

	# define parameters 
	params = {'list':input_genes, 'description':''}

	# make request: post the gene list
	post_response = requests.post( post_url, files=params)

	# load json 
	inst_dict = json.loads( post_response.text )
	userListId = str(inst_dict['userListId'])

	# wait for response 
	print(userListId)

	# return the userListId that is needed to reference the list later 
	return userListId

# make the get request to enrichr using the requests library 
# this is done after submitting post request with the input gene list 
def enrichr_get_request( gmt, num_terms, userListId, inst_color ):
  # get metadata 
	import requests
	import json

	print('inst_color '+ inst_color)

	# define the get url 
	get_url = 'http://amp.pharm.mssm.edu/Enrichr/enrich'

	# get parameters 
	params = {'backgroundType':gmt,'userListId':userListId}

	# make the get request to get the enrichr results 
	get_response = requests.get( get_url, params=params )

	# check that the response is 200 (Okay)
	print(get_response)

	# load as dictionary 
	resp_json = json.loads( get_response.text )

	# get the key 
	only_key = resp_json.keys()[0]

	# get response_list 
	response_list = resp_json[only_key]

	# transfer the response_list to the enr_dict 
	enr = transfer_to_enr_dict( response_list, num_terms, inst_color )

	# return enrichment json and userListId
	return enr 

# transfer the response_list to a list of dictionaries 
def transfer_to_enr_dict(response_list, num_terms, inst_color):

	# reduce the number of enriched terms if necessary
	if len(response_list) < num_terms:
		num_terms = len(response_list)

	# p-value, adjusted pvalue, z-score, combined score, genes 
	# 1: Term 
	# 2: P-value
	# 3: Z-score
	# 4: Combined Score
	# 5: Genes
	# 6: pval_bh

	# transfer response_list to enr structure 
	# and only keep the top terms 
	#
	# initialize enr
	enr = []
	for i in range(num_terms):

		# get list element 
		inst_enr = response_list[i]

		# initialize dict 
		inst_dict = {}

		# transfer term 
		inst_dict['name'] = inst_enr[1]
		# transfer pval
		inst_dict['pval'] = inst_enr[2]
		# transfer zscore
		inst_dict['zscore'] = inst_enr[3]
		# transfer combined_score
		inst_dict['combined_score'] = inst_enr[4]
		# transfer int_genes 
		inst_dict['int_genes'] = inst_enr[5]
		# adjusted pval
		inst_dict['pval_bh'] = inst_enr[6]
		# add the color 
		inst_dict['color'] = inst_color

		# append dict
		enr.append(inst_dict)

	return enr 


