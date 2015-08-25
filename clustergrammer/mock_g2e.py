def main():

	# # generate fake data: 
	# # num_sigs, num_genes, pct_meas
	# gen_fake_g2e_json(30, 200, 1, 0.5 )	

	# load network from G2N example post json 
	make_g2e_clust()


def make_g2e_clust():

	# the main thing to consider is that I need to get the list of genes 
	# from all signatures and then fill in the data using this 
	# I'll simulate slightly overlapping data by generating a master list 
	# of genes and then only randomly 'measure' the expression of these genes 

	# import network class from Network.py
	from d3_clustergram_class import Network

	# get instance of Network  
	net = Network()
	print(net.__doc__)
	print('make tsv clustergram')	

	# load g2e data from file 
	g2e = net.load_json_to_dict('mock_g2e/g2e_post.json')

	# load fake g2e request data to 
	net.load_g2e_to_net(g2e)

	# swap nans for zero 
	net.swap_nan_for_zero()

	# filter the matrix using cutoff and min_num_meet
	###################################################
	cutoff_meet = 0.5
	min_num_meet = 10
	net.filter_network_thresh( cutoff_meet, min_num_meet )

	# cluster 
	#############
	cutoff_comp = 0.25
	min_num_comp = 3	
	net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)


	# # export data visualization to file 
	# ######################################
	# # viz_json = net.export_net_json('viz', 'indent')
	# net.write_json_to_file('viz', 'mock_g2e/g2e_post.json','indent')	

def gen_fake_g2e_json(num_sigs, tot_genes, sig_bias_inf, pct_meas=1):
	# import network class from Network.py
	from d3_clustergram_class import Network

	# get instance of Network  
	net = Network()
	# generate example g2n json 
	##############################
	import string
	import random

	noise_level = 1

	random.seed(12122112312)
	
	g2e = {}
	g2e['tag'] = 'cats'
	g2e['gene_signatures'] = []

	rand_genes = []
	for i in range(tot_genes):
		rand_genes.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)))
		
	sig_bias = {}

	for sig_index in range(num_sigs):
		for gene_index in range(tot_genes):

			if sig_index < num_sigs*0.33 and gene_index < tot_genes*0.33:
				sig_bias[sig_index,gene_index] = sig_bias_inf # * random.random()
			elif sig_index > num_sigs*0.33 and sig_index < num_sigs*0.66 and gene_index > tot_genes*0.33 and gene_index < tot_genes*0.66:
				sig_bias[sig_index,gene_index] = -sig_bias_inf # * random.random() 
			else:
				sig_bias[sig_index,gene_index]= 0


	for i in range(num_sigs):
		for j in range(len(rand_genes)):

			# generate signature object 
			inst_sig = {}

			# set name of signature 
			inst_sig['name'] = 'sig-' + str(i)

			# generate list of genes and values 
			inst_sig['genes'] = []

			# make genes
			for j in range(len(rand_genes)):
					
				# randomly measure only a subset of genes 
				if random.random() < pct_meas:

					# get inst_gene 
					inst_gene = rand_genes[j]

					# generate random value 
					if random.random() < 0.5:
						inst_noise = random.random()
					else:
						inst_noise = -random.random()

					inst_value = sig_bias[(i,j)] + inst_noise*noise_level

					# # swap direction of gene 
					# if random.random() < 0.05:
					# 	inst_value = -inst_value

					inst_list = [ inst_gene, inst_value ]

					# add measurement to list 
					inst_sig['genes'].append(inst_list)

		# append to g2e as signature 
		g2e['gene_signatures'].append(inst_sig)

	# save json 
	net.save_dict_to_json(g2e, 'mock_g2e/g2e_post.json', 'indent')

# run main
main()