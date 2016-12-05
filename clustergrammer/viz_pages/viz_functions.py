from flask import render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import json

def get_network_from_mongo(user_objid, mongo_address):
  client = MongoClient(mongo_address)
  db = client.clustergrammer
  fs = gridfs.GridFS(db)

  try:
    obj_id = ObjectId(user_objid)
  except:
    obj_id = 'error'

  # load object
  if obj_id != 'error':
    net = db.networks.find_one({'_id': obj_id })

    if net['viz'] == 'saved_to_grid_fs':

      # get viz from gridfs
      inst_out = fs.get(net['grid_id'])
      grid_net = inst_out.read()
      grid_net = json.loads(grid_net)
      net['viz'] = grid_net

  else:
    net = 'error'

  # look up sim_row and sim_col if necessary

  for inst_rc in ['sim_row', 'sim_col']:

    if inst_rc in net:

      if type(net[inst_rc]) is not dict:

        inst_id = net[inst_rc]

        found_sim = db.networks.find_one({'_id': inst_id})

        net[inst_rc] = found_sim
        found_sim['_id'] = str(found_sim['_id'])

  client.close()

  return net

def render_page(net, page_route, mat_type='clust'):
  if net != 'error':

    # render sim_mats page
    if page_route == 'viz_sim_mats.html':

      viz_id = str(net['_id'])

      return render_template(page_route, viz_network=net['viz'],
        viz_name=net['name'], viz_sim_row=net['sim_row'],
        viz_sim_col=net['sim_col'], viz_id=viz_id)

    # render viz page
    else:

      if mat_type == 'clust':
        viz_network = net['viz']
      else:
        if mat_type in net:
          viz_network = net[mat_type]
        else:
          viz_network = net['viz']

      return render_template(page_route, viz_network=viz_network,
        viz_name=net['name'])

  else:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)
