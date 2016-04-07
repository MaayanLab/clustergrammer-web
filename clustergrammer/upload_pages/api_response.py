def make_response(mongo_address, viz_id, viz_name, response_type='link'):
  import flask
  import json

  viz_name, viz_url = make_viz_url_name(viz_name)

  response = {}
  response['link'] = viz_url+viz_id+viz_name
  response['id'] = viz_id

  if response_type == 'json':

    viz_doc = get_viz_doc(mongo_address, viz_id)

    response['json'] = json.dumps(viz_doc['viz'])

  return flask.jsonify( response )

def get_viz_doc(mongo_address, viz_id):
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  
  try:
    client = MongoClient(mongo_address)
    db = client.clustergrammer 
    viz_id = ObjectId(viz_id)

    viz_doc = db.networks.find_one({'_id': viz_id })

    if viz_doc == None:
      viz_doc = {}
      viz_doc['viz'] = 'did-not-find-viz'

  except:
    viz_doc = {}
    viz_doc['viz'] = 'did-not-find-viz'

  client.close()   

  return viz_doc  

def make_viz_url_name(viz_name):
  if viz_name == 'gen3va':
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/gen3va/'
    viz_name = ''
  elif viz_name == 'harmonizome':
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/harmonizome/'
    viz_name = ''      
  else:
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'
    viz_name = '/' + viz_name

  return viz_name, viz_url  