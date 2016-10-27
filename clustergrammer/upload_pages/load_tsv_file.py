def main( buff, inst_filename, mongo_address, viz_id, req_sim_mat=False):
  import numpy as np
  import flask
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  from flask import request
  # from clustergrammer import Network
  # from clustergrammer_v120 import Network
  # from clustergrammer_v132 import Network

  # clustergrammer.py version 1.1.2 latest: 10-27-2016
  # version number is different because the python library was separated from
  # the JS library
  from clustergrammer_py_v112 import Network
  import StringIO

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  viz_id = ObjectId(viz_id)
  found_viz = db.networks.find_one({'_id':viz_id})

  print('in load_tsv_file ' + inst_filename)

  # try:
  print('trying to cluster tsv')

  net = Network()
  net.load_tsv_to_net(buff)

  net.swap_nan_for_zero()

  views = ['N_row_sum', 'N_row_var']

  net.make_clust(dist_type='cosine', dendro=True, views=views, \
                 linkage_type='average', sim_mat=req_sim_mat)

  export_dat = {}
  export_dat['name'] = inst_filename
  export_dat['dat'] = net.export_net_json('dat')
  export_dat['source'] = 'user_upload'

  dat_id = db.network_data.insert(export_dat)

  update_viz = net.viz
  update_dat = dat_id

  if req_sim_mat:
    update_sim_row = net.sim['row']
    update_sim_col = net.sim['col']

  # except:
  #   print('\nerror in clustering tsv file\n-------------------------\n')
  #   update_viz = 'error'
  #   update_dat = 'error'
  #   if req_sim_mat:
  #     update_sim_row = 'error'
  #     update_sim_col = 'error'

  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

  if req_sim_mat:

    sim_row_id = db.networks.insert(update_sim_row)
    found_viz['sim_row'] = sim_row_id

    sim_col_id = db.networks.insert(update_sim_col)
    found_viz['sim_col'] = sim_col_id

    # do not directly save sim_row and sim_col to net, save them separately
    # and keep the id with links in net only
    # found_viz['sim_row'] = update_sim_row
    # found_viz['sim_col'] = update_sim_col

  print('updating document ' + inst_filename)
  db.networks.update_one( {'_id':viz_id}, {'$set': found_viz} )

  client.close()


