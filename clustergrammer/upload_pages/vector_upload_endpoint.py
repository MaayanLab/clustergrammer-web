def main(mongo_address):
  from flask import request
  
  vector_post, inst_status, viz_name, viz_id = load_vector_data(request.data, mongo_address)

  if inst_status == 'processing':
    return clust_vector_background(mongo_address, viz_id, vector_post, viz_name)
  else:   
    return make_error_json()

def clust_vector_background(mongo_address, viz_id, vector_post, viz_name):
  import flask
  import run_vector_upload
  import threading 
  import time 

  sub_function = run_vector_upload.main
  arg_list = [ mongo_address, viz_id, vector_post ]
  thread = threading.Thread(target=sub_function, args=arg_list)
  thread.setDaemon(True)

  thread.start()

  response_type = 'link'
  if 'response_type' in vector_post:
    response_type = vector_post['response_type']

  max_wait_time = 30
  for wait_time in range(max_wait_time):

    time.sleep(1)

    if thread.isAlive() is False:

      return make_response(mongo_address, viz_id, viz_name, response_type)

  # did not finish clustering - do not return json 
  return make_response(mongo_address, viz_id, viz_name, response_type='link')

def make_response(mongo_address, viz_id, viz_name, response_type='link'):
  import flask
  from bson.objectid import ObjectId
  from pymongo import MongoClient
  import json

  viz_name, viz_url = make_viz_url_name(viz_name)

  response = {}
  response['link'] = viz_url+viz_id+viz_name
  response['id'] = viz_id

  if response_type == 'json':

    client = MongoClient(mongo_address)
    db = client.clustergrammer 
    viz_id = ObjectId(viz_id)

    viz_doc = db.networks.find_one({'_id': viz_id })

    response['json'] = json.dumps(viz_doc['viz'])
    client.close() 


  return flask.jsonify( response )

def load_vector_data(data, mongo_address):
  import json 
  from pymongo import MongoClient

  try:
    vector_post = json.loads(data)
    inst_status = 'processing'
  except:
    vector_post = None
    inst_status = 'error'

  export_viz = {}
  if 'title' in vector_post:
    if len(vector_post['title']) > 0:
      export_viz['name'] = vector_post['title']
    else:
      export_viz['name'] = 'vector_post'
  else:
    export_viz['name'] = 'vector_post'
    
  export_viz['viz'] = inst_status
  export_viz['dat'] = inst_status
  export_viz['source'] = 'vector_post'

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    post_id = db.network_data.insert( vector_post )
  except:
    post_id = 'vector_post_too_large'

  export_viz['post'] = post_id

  viz_id = db.networks.insert( export_viz ) 
  viz_id = str(viz_id)

  client.close()

  viz_name = export_viz['name']

  return vector_post, inst_status, viz_name, viz_id

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

def make_error_json():
  error_desc = 'Error in processing Enrichr enrichment vectors.'
  return flask.jsonify({
    'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
  })   