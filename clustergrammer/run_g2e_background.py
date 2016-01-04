def main(mongo_address, viz_id, vect_post):
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  from clustergrammer import Network

  # set up database connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer 
  viz_id = ObjectId(viz_id)
  # get placeholder viz data 
  found_viz = db.networks.find_one({'_id': viz_id })

  # initialize export_dat 
  export_dat = {}
  export_viz = {}

  # try to make clustegram using vect_post 
  try:

    # ini network obj 
    net = Network()
    
    # vector endpoint 
    net.load_vect_post_to_net(vect_post)

    # swap nans for zeros
    net.swap_nan_for_zero()

    # cluster g2e using pandas
    # net.fast_mult_views()

    # calculate top views rather than percentage views
    net.N_top_views()

    # export dat 
    try:

      # convert data to list 
      net.dat['mat'] = net.dat['mat'].tolist()
      net.dat['mat_up'] = net.dat['mat_up'].tolist()
      net.dat['mat_dn'] = net.dat['mat_dn'].tolist()

      export_dat['dat'] = net.export_net_json('dat')
      export_dat['source'] = 'g2e_enr_vect'
      dat_id = db.network_data.insert( export_dat )
      print('G2E: network data successfully uploaded')
    
    except:
      export_dat['dat'] = 'data-too-large'
      export_dat['source'] = 'g2e_enr_vect'
      dat_id = db.network_data.insert( export_dat )
      print('G2E: network data too large to be uploaded')

    update_viz = net.viz 
    update_dat = dat_id

  # if there is an error update json with error 
  except:

    print('\n--------------------------------')
    print('G2E clustering error')
    print('----------------------------------\n')
    update_viz = 'error'
    update_dat = 'error'


  # export vix to database 

  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

   # update the viz data 
  try:
    db.networks.update_one( {"_id":viz_id}, {"$set": found_viz} )
    print('\n\n---------------------------------------------------')
    print( 'G2E Successfully made and uploaded clustergram')
    print('---------------------------------------------------\n\n')
  except:
    print('\n--------------------------------')
    print('G2E error in loading viz into database')
    print('----------------------------------\n')

  # close database connection 
  client.close() 


