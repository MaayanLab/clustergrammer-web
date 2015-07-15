# make the requests to enrichr using requests 
def main():

	# input genes
	input_genes = ["CD2BP2", "SLBP", "FOXK2", "STMN2", "SMAD4", "EIF6", "SF1", "CTNND2", "DBN1", "IQGAP2", "P2RX6", "ANKRD6", "C9ORF40", "ARHGEF7", "GOLGA2", "PPME1", "FAM129A", "YES1", "GLI4", "1600027N09RIK", "PTS", "PATL1", "ORAI1", "SPATS2L", "DCX", "HK2", "CSPG4", "AMBRA1", "SENP3", "THOP1", "DSG2", "PER1", "ACLY", "NR1H4", "PTPN7", "BRD2", "TAX1BP1", "RGS14", "SLC40A1", "CNN3", "PLSCR1", "PIP5K1B", "GRB14", "CTR9", "ARHGAP15", "TOM1L2", "ZNF148", "TBC1D12", "BAIAP2", "TOP2A"]

	# run request function 
	enr, userListId = enrichr_request(input_genes, '', 'ChEA' )

	print(enr[0])
	print(userListId)

def enrichr_request( input_genes, meta='', gmt='' ):

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

	# define the get url 
	get_url = 'http://amp.pharm.mssm.edu/Enrichr/enrich'

	# get parameters 
	params = {'backgroundType':gmt,'userListId':userListId}

	# make the get request to get the enrichr results 
	get_response = requests.get( get_url, params=params )

	# load as dictionary 
	resp_json = json.loads( get_response.text )

	# get the key 
	only_key = resp_json.keys()[0]

	enr = resp_json[only_key]

	# return enrichment json and userListId
	return enr, userListId

def enrichr_result(genes, meta='', gmt=''):
	import cookielib, poster, urllib2, json
	import time

	global baseurl
	baseurl = 'amp.pharm.mssm.edu'
	# baseurl = 'matthews-mbp:8080'

	"""return the enrichment results for a specific gene-set library on Enrichr"""
	cj = cookielib.CookieJar()
	opener = poster.streaminghttp.register_openers()
	opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	genesStr = '\n'.join(genes)

	params = {'list':genesStr,'description':meta,'inputMethod':'enrichr_cluster'}
	datagen, headers = poster.encode.multipart_encode(params)
	url = "http://" + baseurl + "/Enrichr/enrich"
	request = urllib2.Request(url, datagen, headers)

	# wait for request 
	resp = urllib2.urlopen(request)

	# # print(resp.read())
	# time.sleep(2)

	# alternate wait for response
	# try:
	# 	resp = urllib2.urlopen(request)
	# 	print(resp.read())
	# except IOError as e:
	# 	pass

	x = urllib2.urlopen("http://" + baseurl + "/Enrichr/enrich?backgroundType=" + gmt)
	response = x.read()
	response_list = json.loads(response)
	return response_list[gmt]


# # run main
# main()