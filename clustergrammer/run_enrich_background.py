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

    print(g2e_post)

    # make clustergram 
    threshold = 0.001
    num_thresh = 1
    # get results from Enrichr and make clustergram netowrk object 
    net = enr_fun.make_enr_vect_clust(g2e_post, threshold, num_thresh)
  
    print('\n\nfinished clustering/n-----------------------\n------------------\n')

    # export dat to database 
    #!! export dat not working 
    export_dat = {}
    print('define export_dat')
    export_dat['name'] = 'enrichment_vector'
    export_dat['dat'] = '' # net.export_net_json('dat')
    export_dat['source'] = 'g2e_enr_vect'
    dat_id = db.network_data.insert( export_dat )

    print('defining update viz and dat ')
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