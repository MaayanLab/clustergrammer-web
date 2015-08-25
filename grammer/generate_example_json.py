# this will generate a json with an example gene list 50 genes long 

def main():
	import json_scripts

	# load gene list text file 
	filename = 'example_gene_50.txt'
	f = open(filename,'r')
	genes_text = f.readlines()
	f.close()

	# clean gene names
	genes_text = [d.strip().upper() for d in genes_text]

	# remove duplicates
	genes_text = list(set(genes_text))

	print(len(genes_text))

	# generate dictionary 
	example_list = {}
	example_list['genes'] = genes_text

	# save to json 
	json_scripts.save_to_json(example_list,'example_gene_50.json','no_indent')

# run main
main()