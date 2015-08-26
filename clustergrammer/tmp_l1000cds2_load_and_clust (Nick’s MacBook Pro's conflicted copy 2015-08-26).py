def main():
  from d3_clustergram_class import Network
 
  # initialize network 
  net = Network()

  # load l1000cds2 json 
  l1000cds2 = net.load_json_to_dict('example_l1000cds2/clsgrm.geneSet.json')

  # load data into network 
  net.load_l1000cds2(l1000cds2)

  # cluster 
  cutoff_comp = 1
  min_num_comp = 2
  net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)  

  # generate export dictionary 
  ###############################
  export_dict = {}
  # save name of network 
  export_dict['name'] = 'tmp'
  # initial network information, including data_mat array
  export_dict['dat'] = net.dat
  # d3 json used for visualization (already clustered)
  export_dict['viz'] = net.viz

  # # set up connection 
  # client = MongoClient('146.203.54.165')
  # db = client.clustergrammer

  # # save json as new collection 
  # ##################################
  # print('loading data to matrix')
  # tmp_id = db.networks.insert( export_dict ) 

  # # make net_id a string
  # tmp_id = str(tmp_id)

  # # close client
  # client.close()

  # # return id only 
  # return tmp_id, net

main()