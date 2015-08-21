
def load_file(req_file, allowed_file):

  import numpy as np
  import flask
  import make_exp_clustergram
  from pymongo import MongoClient
  from flask import request
  # import network class from Network.py
  from d3_clustergram_class import Network

  # initiate class network 
  net = Network()

  # set up connection 
  client = MongoClient()
  db = client.clustergrammer

  # get the filename 
  inst_filename = req_file.filename
  
  # check that request is a post
  if request.method == 'POST' and allowed_file(inst_filename):

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
    cutoff_comp = 0
    min_num_comp = 2
    net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)


    # convert data matrix to list 
    net.dat['mat'] = net.dat['mat'].tolist()
    net.dat['node_info'] = []

    # generate export dictionary 
    ###############################
    export_dict = {}
    # save name of network 
    export_dict['name'] = inst_filename
    # initial network information, including data_mat array
    export_dict['dat'] = net.dat
    # d3 json used for visualization (already clustered)
    export_dict['viz'] = net.viz

    # save json as new collection 
    ##################################
    tmp_id = db.networks.insert( export_dict ) 
    print(tmp_id)

    # close client
    client.close()

    # return the network in json form 
    # return flask.jsonify(d3_json)
    return flask.jsonify(net.viz)

  else:
    print('error in file upload - check filetype')

    return error