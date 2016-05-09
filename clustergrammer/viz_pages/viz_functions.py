from flask import render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

def get_network_from_mongo(user_objid, mongo_address):
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    obj_id = 'error'

  if obj_id != 'error':
    net = db.networks.find_one({'_id': obj_id })
  else:
    net = 'error'

  client.close()

  return net

def render_page(net, page_route, mat_type='three_mats'):
  print('\nrender page\t'+str(mat_type)+'\n-----------------------------')
  if net != 'error':

    print(net.keys())

    if page_route == 'viz_sim_mats.html':

      viz_id = str(net['_id'])

      return render_template(page_route, viz_network=net['viz'], 
        viz_name=net['name'], viz_sim_row=net['sim_row'], 
        viz_sim_col=net['sim_col'], viz_id=viz_id)

    elif page_route == 'viz.html':

      if mat_type == 'clust':
        viz_network = net['viz']
      elif mat_type == 'sim_row':
        viz_network = net['sim_row']
      elif mat_type == 'sim_col':
        viz_network = net['sim_col']

      return render_template(page_route, viz_network=viz_network, 
        viz_name=net['name'])
  else:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)  
