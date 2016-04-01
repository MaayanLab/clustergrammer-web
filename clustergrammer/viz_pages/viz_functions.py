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

def render_page(net, page_route):
  if net != 'error':
    return render_template(page_route, viz_network=net['viz'], viz_name=net['name'])
  else:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)  
