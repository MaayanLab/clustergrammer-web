
def main(req_file, allowed_file, mongo_address):

  import numpy as np
  import flask
  import make_exp_clustergram
  from pymongo import MongoClient
  from flask import request
  # import network class from Network.py
  from d3_clustergram_class import Network
  import StringIO
  # import pandas as pd
  from copy import deepcopy

  print('\n\n\nLoading File\n###########\n\n\n')

  # initiate class network 
  net_view = Network()

  # get the filename 
  inst_filename = req_file.filename

  print('\n\ninst_filename')
  print(inst_filename)
  
  # # read data using pandas 
  # buff = StringIO.StringIO(req_file.read())
  # df = pd.read_table(buff, index_col=0)
  # # load dataframe to network dat 
  # net_view.df_to_dat(df)

  # read file
  lines = req_file.readlines()

  print(lines)

  net_view.load_lines_from_tsv_to_net(lines)  

  print('finished loading lines from tsv')

  # swap nans for zero 
  net_view.swap_nan_for_zero()

  # pre-filter matrix 
  ######################
  cutoff_meet = 0.001
  min_num_meet = 2
  net_view.filter_network_thresh( cutoff_meet, min_num_meet )

  net_view.viz['views'] = []

  all_views = []

  # calc mult_views of clustergram 
  ######################################

  # filter between 0 and 90% of max value 
  all_filt = range(10)
  all_filt = [i/float(10) for i in all_filt]

  mat = net_view.dat['mat']
  max_mat = max(mat.min(), mat.max(), key=abs)

  inst_meet = 1

  for inst_filt in all_filt:

    print('\ninst_filt\t'+str(inst_filt))

    # load network from tsv file
    ##############################
    net = deepcopy(Network())

    net.dat = deepcopy(net_view.dat)

    filt_value = inst_filt * max_mat

    net.filter_network_thresh(filt_value,inst_meet)

    mat_shape = net.dat['mat'].shape

    try:
      # cluster
      #############
      # only compare vectors with at least min_num_comp common data points
      # with absolute values above cutoff_comp
      net.cluster_row_and_col('cos')

      # add view 
      inst_view = {}
      inst_view['filt'] = inst_filt
      inst_view['num_meet'] = inst_meet
      inst_view['dist'] = 'cos'
      inst_view['nodes'] = {}
      inst_view['nodes']['row_nodes'] = net.viz['row_nodes']
      inst_view['nodes']['col_nodes'] = net.viz['col_nodes']

      all_views.append(inst_view)

    except:
      print('\n\ndo not make clustergram\n\n')

  # add views to viz
  net_view.viz['views'] = all_views



  # cluster 
  #############
  print('clustering')
  net_view.cluster_row_and_col('cos')

  # convert data matrix to list 
  # net_view.dat['mat'] = net_view.dat['mat'].tolist()

  print('clear node_info')
  net_view.dat['node_info'] = []

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
  export_dat['dat'] = net_view.export_net_json('dat')
  export_dat['source'] = 'user_upload'

  # save dat to separate document 
  dat_id = db.network_data.insert(export_dat)

  # save name of network 
  export_viz['name'] = inst_filename
  # save visualization json 
  export_viz['viz'] = net_view.viz
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
  return tmp_id, net_view

  