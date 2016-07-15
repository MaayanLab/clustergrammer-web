def Enrichr_cluster(mongo_address, viz_id, enr_list):
  import enrichr_functions as enr_fun
  from bson.objectid import ObjectId
  from pymongo import MongoClient

  # set up database connection
  client = MongoClient(mongo_address)
  db = client.clustergrammer
  viz_id = ObjectId(viz_id)
  # get placeholder viz data
  found_viz = db.networks.find_one({'_id': viz_id })

  # try to get enr and make clustergram
  try:

    # make clustergram
    threshold = 0.001
    num_thresh = 1
    # get results from Enrichr and make clustergram netowrk object
    net = enr_fun.enrichr_clust_from_response(enr_list)

    # export dat to database
    #!! export dat not working
    export_dat = {}
    export_dat['name'] = 'enrichment_vector'
    export_dat['dat'] = '' # net.export_net_json('dat')
    export_dat['source'] = 'Enrichr_clustergram'
    dat_id = db.network_data.insert( export_dat )

    update_viz = net.viz
    update_dat = dat_id

  # if there is an error update json with error
  except:

    update_viz = 'error'
    update_dat = 'error'


  # export viz to database
  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

  # update the viz data
  db.networks.update_one( {"_id":viz_id}, {"$set": found_viz} )

  # close database connection
  client.close()
