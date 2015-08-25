# the general code to do enrichment analysis using an input_list and a gmt 
# input_list: a list of genes
# input_gmt: a dict of gmt terms and associated lists of genes 
def calc(input_list, input_gmt):

	# import scipy to calculate fisher exact test 
	from scipy import stats
	# import operator module 
	from operator import itemgetter


	# calculate the total number of genes in the gmt 
	num_genes, all_genes = calc_num_genes_GMT(input_gmt)

	# input_genes: only include genes that are cound in the gmt 
	input_genes = list(set(all_genes).intersection( input_list ))

	# initialize array of enrichment results
	enr_results = []

	# loop through the lines of the GMT 
	for key in input_gmt:

		# check if any of the input genes are in the current line of the GMT 
		# if there are none, then this term cannot be enriched 
		if len( list(set(input_genes).intersection(input_gmt[key])) ):

			# grab the elements from the gmt file 
			elems = input_gmt[key]
 
			# save the intersecting genes 
			int_genes = list(set(input_genes).intersection(set(elems)))

			# number of input genes found in GMT elements
			a = len(int_genes)
			# number of input genes not foung in the GMT elements 
			b = len(input_genes) - a
			# number of genes in the current gmt line 
			c = len(elems)
			# total number of genes in the GMT file minus the number of genes in the current GMT line 
			d = num_genes - c

			# calculate the fisher exact test 
			oddsratio, pvalue = stats.fisher_exact([[a,b], [c,d]])

			# save to array of dictionaries 
			#################################
			# append dictionaries to array 
			enr_results.append(dict({'name': key, 'pval': pvalue, 'int_genes': int_genes}))

	# order the enrichment results by ascending pvals (smallest first)
	enr_results = sorted(enr_results, key=itemgetter('pval') )

	# correct pvals 
	enr_results = correct_pval(enr_results)

	return enr_results

# correct the pvals, Bonferroni, Benjamini-Hochberg 
def correct_pval(enr_drug):

	# load operator module 
	from operator import itemgetter

	# sort enrichment results based on descending pvalue - to correct the pvals
	enr_drug = sorted( enr_drug, key=itemgetter('pval'), reverse=True )

	# the number of comparisons made is equal to the number of pvals calculated 
	list_count = len(enr_drug)

	# initialize the values 
	prev_val = 1

	# initialize the list_count 
	current_list_count = list_count

	# loop through the pvals 
	for i in range(list_count):

		# Bonferonni correction (add value as a new dict value)
		# multiply the pval by the number of comparisons made 
		enr_drug[i]['pval_bon'] = enr_drug[i]['pval'] * list_count

		# initial bh correction 
		bh_adjusted = enr_drug[i]['pval'] * list_count / current_list_count

		# preserve monotonicity 
		if bh_adjusted > prev_val:

			# if the current bh adjusted pval is greater than teh previous one then
			# set it to be equal to the previous value 
			bh_adjusted = prev_val 

		# save the current adjusted pval as the previous pval
		prev_val = bh_adjusted

		# save the value to the data structure 
		enr_drug[i]['pval_bh'] = bh_adjusted

		# lower the current list count as part of the bh correction 
		current_list_count = current_list_count - 1

	# reorder the enrichment results in ascending order 
	enr_drug = sorted( enr_drug, key=itemgetter('pval'), reverse=False )

	#! keep all the enriched drugs, for now 
	# # keep only the top 20 enriched drugs 
	# enr_drug = enr_drug[0:20]

	# return the corrected enrichment list of dictionaries 
	return enr_drug

# calculate the total number of genes in the gmt
def calc_num_genes_GMT(ks_gmt):

	# initialize the list of all genes 
	all_genes = []

	# calc the toal number of genes in the GMT file 
	for key in ks_gmt:

		# append genes into one list 
		all_genes.extend(ks_gmt[key])

	# get unique genes 
	all_genes = list(set(all_genes))

	# # 367
	# print( '\nthere are ' + str(len(all_genes)) + ' kinases\n' )

	# num unique genes 
	num_genes = len(all_genes)

	return num_genes, all_genes

# load a gmt 
# this will make a dict with terms and associated gene lists
# if the file is in the normal gmt format
def load_gmt(filename):

	# load kinomescan gmt file 
	f = open(filename, 'r')
	kinomescan_data = f.readlines()
	f.close()

	# generate a dict from the gmt 
	#

	# initialize the kinomescan_gmt dict 
	inst_gmt = {}

	# loop through the lines of the gmt 
	for i in range(len(kinomescan_data)):

		# get the inst line, strip off the new line character 
		inst_line = kinomescan_data[i].strip()

		# get the drug name 
		inst_drug = inst_line.split('\t')[0]

		# get the kinases in the set (the second column is not a kinase)
		inst_kinases = inst_line.split('\t')[2:]

		# save the drug-kinase sets 
		inst_gmt[inst_drug] = inst_kinases

	return inst_gmt

# convert json to gmt 
def json_2_gmt(filename):
	import json_scripts

	# load json 
	inst_json = json_scripts.load_to_dict(filename)

	# get sorted dict keys 
	all_keys = sorted( inst_json.keys() )

	# write gmt 
	###############
	# convert filename to .gmt 
	filename = filename.split('.')[0] + '.gmt'
	fw = open(filename, 'w')

	# loop through keys 
	for inst_key in all_keys:

		# get gene list 
		inst_list = inst_json[inst_key]

		# print( inst_key + '\t' + str(len(inst_list)) + '\n' )

		# write line of gmt 
		fw.write(inst_key + '\tna\t' )

		# write genes 
		for inst_elem in inst_list:
			fw.write(inst_elem + '\t')
		
		# write new line 
		fw.write('\n')

	fw.close()