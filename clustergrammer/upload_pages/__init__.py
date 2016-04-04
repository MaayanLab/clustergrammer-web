from flask import Blueprint, render_template, request
from flask.ext.cors import cross_origin
from pymongo import MongoClient

import Enrichr_clustergram_endpoint as enr_clust_endpoint

def add_routes(app=None, mongo_address=None):

  upload_pages = Blueprint('upload_pages', __name__, 
    static_url_path='/upload_pages/static', static_folder='./static', 
    template_folder='./templates')

  @upload_pages.route('/clustergrammer/Enrichr_clustergram', methods=['POST','GET'])
  @cross_origin()
  def enrichr_clustergram():

    return enr_clust_endpoint.main(mongo_address)

  @upload_pages.route('/clustergrammer/vector_upload/', methods=['POST'])
  @cross_origin()
  def proc_vector_upload():
    import requests 
    import flask
    import json 
    from clustergrammer import Network
    import threading 
    import time 
    import run_g2e_background

    try:
      vector_post = json.loads(request.data)
      inst_status = 'processing'
    except:
      inst_status = 'error'

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

        # wait one second 
        time.sleep(1)

        print('\twaiting '+str(wait_time)+' is alive '+str(thread.isAlive()))

        if thread.isAlive() == False:

          print('thread is finished')
          
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

  app.register_blueprint(upload_pages)