def main(mongo_address):
  
  import requests 
  import flask
  from flask import request
  import threading 
  import time 
  from pymongo import MongoClient
  
  from clustergrammer import Network
  import run_g2e_background

  vector_post, inst_status = load_response_data(request.data)

  client = MongoClient(mongo_address)
  db = client.clustergrammer

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

  try: 
    post_id = db.network_data.insert( vector_post )
  except:
    post_id = 'vector_post_too_large'

  export_viz['post'] = post_id

  viz_id = db.networks.insert( export_viz ) 
  viz_id = str(viz_id)

  client.close()

  if inst_status == 'processing':

    sub_function = run_g2e_background.main
    arg_list = [ mongo_address, viz_id, vector_post ]
    thread = threading.Thread(target=sub_function, args=arg_list)
    thread.setDaemon(True)

    thread.start()

    if export_viz['name'] == 'gen3va':
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/gen3va/'
      inst_name = ''
    elif export_viz['name'] == 'harmonizome':
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/harmonizome/'
      inst_name = ''      
    else:
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'
      inst_name = '/'+export_viz['name']

    max_wait_time = 30
    for wait_time in range(max_wait_time):

      time.sleep(1)

      if thread.isAlive() == False:

        return flask.jsonify({
          'link': viz_url+viz_id+inst_name,
          'id':viz_id
          })

    return flask.jsonify({
      'link': viz_url+viz_id+inst_name,
      'id':viz_id
      })

  else:   

    error_desc = 'Error in processing Enrichr enrichment vectors.'

    return flask.jsonify({
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
    }) 


def load_response_data(data):
  import json 
  try:
    vector_post = json.loads(data)
    inst_status = 'processing'
  except:
    vector_post = None
    inst_status = 'error'

  return vector_post, inst_status