def main(mongo_address, viz_id, vect_post):
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  from clustergrammer import Network

  client = MongoClient(mongo_address)
  db = client.clustergrammer 
  viz_id = ObjectId(viz_id)

  found_viz = db.networks.find_one({'_id': viz_id })

  export_viz = {}

  try:
    net = Network()
    net.load_vect_post_to_net(vect_post)
    net.swap_nan_for_zero()
    net.make_filtered_views(dist_type='cosine', dendro=True, \
      views=['N_row_sum'], linkage_type='average')

    dat_id = upload_dat(db, net)

    update_viz = net.viz 
    update_dat = dat_id

  except:
    print('error clustering')
    update_viz = 'error'
    update_dat = 'error'


  found_viz['viz'] = update_viz
  found_viz['dat'] = update_dat

  try:
    db.networks.update_one( {"_id":viz_id}, {"$set": found_viz} )
  except:
    print('G2E error in loading viz into database')

  client.close() 

def upload_dat(db, net):
  export_dat = {}

  try:
    export_dat['dat'] = make_export_dat(net)
    export_dat['source'] = 'g2e_enr_vect'
    dat_id = db.network_data.insert( export_dat )

  except:
    print('error upload_dat')
    export_dat['dat'] = 'data-too-large'
    export_dat['source'] = 'g2e_enr_vect'
    dat_id = db.network_data.insert( export_dat )  

def make_export_dat(net):
  net.dat['mat'] = net.dat['mat'].tolist()
  net.dat['mat_up'] = net.dat['mat_up'].tolist()
  net.dat['mat_dn'] = net.dat['mat_dn'].tolist()
  return net.export_net_json('dat')