def main(mongo_address):
  from flask import request, current_app
  
  vector_post, inst_status, viz_name, viz_id = load_vector_data(request.data, mongo_address)

  if inst_status == 'processing':
    return clust_vector_background(mongo_address, viz_id, vector_post, viz_name)
  else:   
    return make_error_json(current_app.config)

def clust_vector_background(mongo_address, viz_id, vector_post, viz_name):
  import flask
  import threading 
  import time 
  import run_vector_upload, api_response

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

      return api_response.make_response(mongo_address, viz_id, viz_name, response_type)

  # did not finish clustering - do not return json 
  return api_response.make_response(mongo_address, viz_id, viz_name, response_type='link')

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

def make_error_json(app_config):
  from flask import jsonify
  error_desc = 'Error in processing Enrichr enrichment vectors.'
  return jsonify({
    'link': app_config['ORIGIN'] + app_config['ENTRY_POINT'] + '/error/' + error_desc
  }) 