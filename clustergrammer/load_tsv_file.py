def main( buff, inst_filename, mongo_address, viz_id):
  import numpy as np
  import flask
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  from flask import request
  from clustergrammer import Network
  import StringIO

  ##############################
  # set up database connection 
  ##############################
  # set up connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  # get placeholder viz data 
  viz_id = ObjectId(viz_id)
  found_viz = db.networks.find_one({'_id':viz_id})

  try:
    ########################
    # load and cluster 
    ########################

    # initiate class network 
    net = Network()
    # net.load_lines_from_tsv_to_net(file_lines)  
    net.pandas_load_tsv_to_net(buff)

    # swap nans for zero 
    net.swap_nan_for_zero()

    # pre-filter matrix 
    ######################
    cutoff_meet = 0.001
    min_num_meet = 1
    net.filter_network_thresh( cutoff_meet, min_num_meet )

    # fast mult views takes care of pre-filtering
    net.fast_mult_views()

    ###############################
    # save to database 
    ###############################

    export_dat = {}
    export_dat['name'] = inst_filename
    export_dat['dat'] = net.export_net_json('dat')
    export_dat['source'] = 'user_upload'
    # save dat to separate document 
    dat_id = db.network_data.insert(export_dat)

    update_viz = net.viz 
    update_dat = dat_id

  except:
    print('\n-----------------------')
    print('error in clustering')
    print('-----------------------\n')
    update_viz = 'error'
    update_dat = 'error'

  # update found_viz 
  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

  # update found_viz in database 
  db.networks.update_one( {'_id':viz_id}, {'$set': found_viz} )

  ############################
  # end database connection 
  ############################
  client.close()


  