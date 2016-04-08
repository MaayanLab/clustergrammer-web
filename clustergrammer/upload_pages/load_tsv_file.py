def main( buff, inst_filename, mongo_address, viz_id):
  import numpy as np
  import flask
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  from flask import request
  from clustergrammer import Network
  import StringIO

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  viz_id = ObjectId(viz_id)
  found_viz = db.networks.find_one({'_id':viz_id})

  try:

    net = Network()
    net.load_tsv_to_net(buff)

    net.swap_nan_for_zero()

    views = ['N_row_sum', 'N_row_var']

    net.make_clust(dist_type='cosine', dendro=True, views=views, \
                   linkage_type='average')

    export_dat = {}
    export_dat['name'] = inst_filename
    export_dat['dat'] = net.export_net_json('dat')
    export_dat['source'] = 'user_upload'

    dat_id = db.network_data.insert(export_dat)

    update_viz = net.viz 
    update_dat = dat_id

  except:
    print('\n-----------------------')
    print('error in clustering')
    print('-----------------------\n')
    update_viz = 'error'
    update_dat = 'error'

  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

  db.networks.update_one( {'_id':viz_id}, {'$set': found_viz} )

  client.close()


  