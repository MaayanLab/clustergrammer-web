def main(mongo_address):
  
  # import requests 
  import flask
  from flask import request
  
  # from clustergrammer import Network

  vector_post, inst_status, export_viz, viz_id = load_response_data(request.data, mongo_address)

  if inst_status == 'processing':

    return run_vector_clust(mongo_address, viz_id, vector_post, export_viz)

  else:   

    error_desc = 'Error in processing Enrichr enrichment vectors.'

    return flask.jsonify({
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
    }) 

def run_vector_clust(mongo_address, viz_id, vector_post, export_viz):
  import flask
  import run_vector_upload
  import threading 
  import time 

  sub_function = run_vector_upload.main
  arg_list = [ mongo_address, viz_id, vector_post ]
  thread = threading.Thread(target=sub_function, args=arg_list)
  thread.setDaemon(True)

  thread.start()

  viz_name, viz_url = make_viz_url_name(export_viz)

  max_wait_time = 30
  for wait_time in range(max_wait_time):

    time.sleep(1)

    if thread.isAlive() is False:

      return flask.jsonify({
        'link': viz_url+viz_id+viz_name,
        'id':viz_id
        })

  return flask.jsonify({
    'link': viz_url+viz_id+viz_name,
    'id':viz_id
    })  

def load_response_data(data, mongo_address):
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


  return vector_post, inst_status, export_viz, viz_id

def make_viz_url_name(export_viz):
  if export_viz['name'] == 'gen3va':
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/gen3va/'
    viz_name = ''
  elif export_viz['name'] == 'harmonizome':
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/harmonizome/'
    viz_name = ''      
  else:
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'
    viz_name = '/'+export_viz['name']  

  return viz_name, viz_url

