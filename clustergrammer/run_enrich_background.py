def enr_and_make_viz(mongo_address, viz_id, g2e_post):
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
    net = enr_fun.make_enr_vect_clust(g2e_post, threshold, num_thresh)
  
    # export dat to database 
    export_dat = {}
    export_dat['name'] = 'enrichment_vector'
    export_dat['dat'] = net.export_net_json('dat')
    export_dat['source'] = 'g2e_enr_vect'
    dat_id = db.network_data.insert( export_dat )

    # set up export viz and dat from clustergram result 
    export_viz = net.viz 
    export_dat = dat_id

  # if there is an error update json with error 
  except:

    export_viz = 'error'
    export_dat = 'error'


  # export viz to database 
  found_viz['viz'] = export_viz
  found_viz['dat'] = export_dat

  # update the viz data 
  db.networks.update_one( {"_id":viz_id}, {"$set": found_viz} )

  # close database connection 
  client.close()