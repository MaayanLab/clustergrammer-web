
def main(req_file, allowed_file, mongo_address):

  import numpy as np
  import flask
  from pymongo import MongoClient
  from flask import request
  # import network class from Network.py
  from clustergrammer import Network
  import StringIO
  # import pandas as pd
  from copy import deepcopy

  print('\n\n\nLoading File\n###########\n\n\n')

  # initiate class network 
  net = Network()

  # get the filename 
  inst_filename = req_file.filename

  # # read data using pandas 
  # buff = StringIO.StringIO(req_file.read())
  # df = pd.read_table(buff, index_col=0)
  # # load dataframe to network dat 
  # net.df_to_dat(df)

  # read file
  lines = req_file.readlines()

  net.load_lines_from_tsv_to_net(lines)  

  # swap nans for zero 
  net.swap_nan_for_zero()

  # pre-filter matrix 
  ######################
  cutoff_meet = 0.001
  min_num_meet = 1
  net.filter_network_thresh( cutoff_meet, min_num_meet )

  net.make_mult_views(dist_type='cos',filter_row=True)

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
  return tmp_id, inst_filename

  