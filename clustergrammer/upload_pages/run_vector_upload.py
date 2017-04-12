def main(mongo_address, viz_id, vector_post):
  from bson.objectid import ObjectId
  from pymongo import MongoClient

  client = MongoClient(mongo_address)
  db = client.clustergrammer
  viz_id = ObjectId(viz_id)

  viz_doc = db.networks.find_one({'_id': viz_id })

  viz_doc = clust_vect(db, viz_doc, vector_post)

  update_doc_on_mongo(db, viz_id, viz_doc)

  client.close()

def clust_vect(db, viz_doc, vector_post):

  # from clustergrammer import Network
  from clustergrammer_py_v112_vect_post_fix import Network
  # from clustergrammer_py_v1_13_2 import Network

  try:
    net = Network()
    net.load_vect_post_to_net(vector_post)
    net.swap_nan_for_zero()

    # default views
    views = ['N_row_sum', 'N_row_var']

    if 'views' in vector_post:
      views = vector_post['views']


    net.make_clust(dist_type='cosine', dendro=True, views=views,
                  linkage_type='average')

    dat_id = upload_dat(db, net)

    update_viz = net.viz
    update_dat = dat_id

  except:
    print('error clustering')
    update_viz = 'error'
    update_dat = 'error'

  viz_doc['viz'] = update_viz
  viz_doc['dat'] = update_dat

  return viz_doc

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

def update_doc_on_mongo(db, viz_id, viz_doc):
  try:
    db.networks.update_one( {"_id":viz_id}, {"$set": viz_doc} )
  except:
    print('G2E error in loading viz into database')