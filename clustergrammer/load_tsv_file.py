
def main(req_file, allowed_file, mongo_address):

  import numpy as np
  import flask
  import make_exp_clustergram
  from pymongo import MongoClient
  from flask import request
  # import network class from Network.py
  from d3_clustergram_class import Network

  print('\n\n\nLoading File\n###########\n\n\n')

  # initiate class network 
  net = Network()

  # get the filename 
  inst_filename = req_file.filename
  
  # read file
  lines = req_file.readlines()

  net.load_lines_from_tsv_to_net(lines)

  # # swap nans for zero 
  # net.swap_nan_for_zero()

  # filter the matrix using cutoff and min_num_meet
  ###################################################
  cutoff_meet = 0.01
  min_num_meet = 2
  net.filter_network_thresh( cutoff_meet, min_num_meet )

  # cluster 
  #############
  print('clustering')
  net.cluster_row_and_col('cos')

  # convert data matrix to list 
  # net.dat['mat'] = net.dat['mat'].tolist()

  print('clear node_info')
  net.dat['node_info'] = []

  # set up connection 
  client = MongoClient(mongo_address)
  # client = MongoClient('192.168.2.7')
  db = client.clustergrammer

  # generate export dictionary 
  ###############################
  # initial network information, including data_mat array
  export_viz = {}
  export_dat = {}
  
  export_dat['name'] = inst_filename
  export_dat['dat'] = net.export_net_json('dat')
  export_dat['source'] = 'user_upload'

  # save dat to separate document 
  dat_id = db.network_data.insert(export_dat)

  # save name of network 
  export_viz['name'] = inst_filename
  # save visualization json 
  export_viz['viz'] = net.viz
  # save link to dat 
  export_viz['dat'] = dat_id
  export_viz['source'] = 'user_upload'

  # save json as new collection 
  ##################################
  print('loading data to mongo')
  tmp_id = db.networks.insert( export_viz ) 

  # make net_id a string
  tmp_id = str(tmp_id)

  # close client
  client.close()

  # return id only 
  return tmp_id, net

  