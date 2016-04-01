
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import send_from_directory
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from flask.ext.cors import cross_origin

import viz_pages
import home_pages
import demo_pages
import enrichr_clust

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/clustergrammer'

# address for mongodbs 

# local
mongo_address = '192.168.1.5'

# # lab 
# mongo_address = '146.203.54.165'

##########################################
# switch for local and docker development 
# docker_vs_local
##########################################

# for local development 
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/clustergrammer/clustergrammer' 

# # for docker development
# SERVER_ROOT = '/app/clustergrammer'
# # change routing of logs when running docker 
# logging.basicConfig(stream=sys.stderr) 

######################################
######################################

# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route(ENTRY_POINT + '/<path:path>') 
def send_static(path):
  return send_from_directory(SERVER_ROOT, path)

@app.route('/clustergrammer/status_check/<user_objid>')
def status_check(user_objid):
  import flask
  from bson.objectid import ObjectId

  # initialize status 
  inst_status = 'error'

  # get object id 
  try:
    obj_id = ObjectId(user_objid)
  except:
    inst_status = 'invalid id'
    return inst_status

  # set up db connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  # find object 
  net = db.networks.find_one({'_id': obj_id })
  client.close()

  # check if processing or error 
  if net['viz'] == 'processing':
    inst_status = 'processing'
  elif net['viz'] == 'error':
    inst_status = 'error'
  elif type(net['viz'] is dict):
    inst_status = 'finished'
    
  return inst_status

@app.route("/clustergrammer/l1000cds2/<user_objid>")
def viz_l1000cds2(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  # set up connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    error_desc = 'Invalid L1000CDS2 visualization ID '
    return redirect('/clustergrammer/error/'+error_desc)

  gnet = db.networks.find_one({'_id': ObjectId(user_objid) })

  # close connection 
  client.close()
  d3_json = gnet['viz']

  print('\n\nloading from mongodb\n##################\n')

  return render_template('l1000cds2.html', viz_network=d3_json)

@app.route('/clustergrammer/vector_upload/', methods=['POST'])
@cross_origin()
def proc_vector_upload():
  import requests 
  import flask
  import json 
  from clustergrammer import Network
  import threading 
  import time 
  import run_g2e_background

  print('\n\n\nG2E endpoint\n\n\n')

  # load data from json 
  try:
    vector_post = json.loads(request.data)
    inst_status = 'processing'
  except:
    inst_status = 'error'

  # submit placeholder to mongo 
  ###############################
  # set up connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  export_viz = {}
  if 'title' in vector_post:
    # use if valid title 
    if len(vector_post['title']) > 0:
      export_viz['name'] = vector_post['title']
    else:
      export_viz['name'] = 'vector_post'
  else:
    export_viz['name'] = 'vector_post'
    
  export_viz['viz'] = inst_status
  export_viz['dat'] = inst_status
  export_viz['source'] = 'vector_post'


  # save the posted json 
  try: 
    post_id = db.network_data.insert( vector_post )
  except:
    post_id = 'vector_post_too_large'

  # export_viz['post'] = vector_post
  export_viz['post'] = post_id

  # get the id tht will be used to update the placeholder 
  viz_id = db.networks.insert( export_viz ) 
  viz_id = str(viz_id)

  client.close()

  # start processing if the vector_post json was loaded correctly
  if inst_status == 'processing':

    # initialize thread
    ########################
    sub_function = run_g2e_background.main
    arg_list = [ mongo_address, viz_id, vector_post ]
    thread = threading.Thread(target=sub_function, args=arg_list)
    thread.setDaemon(True)

    # run subprocess 
    ###################
    print('initializing thread to process g2e')
    thread.start()

    # define information return link - always return the same linke
    if export_viz['name'] == 'gen3va':
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/gen3va/'
      inst_name = ''
    elif export_viz['name'] == 'harmonizome':
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/harmonizome/'
      inst_name = ''      
    else:
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'
      inst_name = '/'+export_viz['name']

    # check if subprocess is finished 
    ###################################
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

    # return link after max time has elapsed 
    return flask.jsonify({
      'link': viz_url+viz_id+inst_name,
      'id':viz_id
      })

  else:   

    error_desc = 'Error in processing Enrichr enrichment vectors.'

    return flask.jsonify({
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
    }) 

@app.route('/clustergrammer/l1000cds2/', methods=['POST'])
def l1000cds2_upload():
  import requests
  import json 
  from clustergrammer import Network 
  from pymongo import MongoClient
  from bson.objectid import ObjectId

  # get the json 
  l1000cds2 = json.loads( request.form.get('signatures') )

  # initialize network 
  net = Network()

  # load l1000cds2 to .dat 
  net.load_l1000cds2(l1000cds2)

  # cluster 
  cutoff_comp = 0
  min_num_comp = 2
  net.cluster_row_and_col(dist_type='cosine', dendro=True)  

  # redefine initial ordering - rank by gene signature values and pert scores 
  net.dat['node_info']['row']['ini'] = net.sort_rank_node_values('row')
  net.dat['node_info']['col']['ini'] = net.sort_rank_node_values('col')
  net.viz = {}
  net.viz['row_nodes'] = []
  net.viz['col_nodes'] = []
  net.viz['links'] = []
  # remake visualization 
  net.viz_json()

  # generate export dictionary 
  ###############################
  export_dict = {}
  export_dict['name'] = 'l1000cds2'
  export_dict['dat'] = net.export_net_json('dat')
  export_dict['viz'] = net.viz
  export_dict['_id'] = ObjectId(l1000cds2['_id'])
 
  # set up connection 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  # save to database 
  ##################################
  tmp = db.networks.find_one({'_id': ObjectId(l1000cds2['_id']) })
  if tmp is None:
    tmp_id = db.networks.insert( export_dict ) 

  # close client
  client.close()

  return redirect('/clustergrammer/l1000cds2/'+l1000cds2['_id'])

@app.route('/clustergrammer/upload_network/', methods=['POST'])
def upload_network():
  import flask 
  import load_tsv_file
  import threading
  import time
  import StringIO

  if request.method == 'POST':

    req_file = flask.request.files['file']
    buff = StringIO.StringIO(req_file.read())

    inst_filename = req_file.filename 

    print('\ninst_filename '+inst_filename+'\n\n')

    if allowed_file(inst_filename):

      # submit placeholder to mongo 
      ###############################
      # set up database connection 
      client = MongoClient(mongo_address)
      db = client.clustergrammer

      # generate placeholder json - does not contain viz json 
      export_viz = {}
      export_viz['name'] = inst_filename
      export_viz['viz'] = 'processing'
      export_viz['dat'] = 'processing'
      export_viz['source'] = 'user_upload'

      # get the id that will be used to update the placeholder 
      viz_id = db.networks.insert( export_viz )
      viz_id = str(viz_id)

      client.close()

      # initialize thread 
      #######################
      print('initializing thread - uploading network')
      sub_function = load_tsv_file.main
      arg_list = [ buff, inst_filename, mongo_address, viz_id]
      thread = threading.Thread(target=sub_function, args=arg_list)
      thread.setDaemon(True)

      # run subprocess
      ##################
      thread.start()

      ####################
      # check subprocess 
      ####################
      max_wait_time = 15
      for wait_time in range(max_wait_time):

        # wait one second
        time.sleep(1)

        print(wait_time)
        print(thread.isAlive())

        if thread.isAlive() == False:

          print('\n\nthread is dead ... job finished\n-------------------\n')

          return redirect('/clustergrammer/viz/'+viz_id+'/'+inst_filename)

      # redirect after maximum time has elapsed 
      return redirect('/clustergrammer/viz/'+viz_id+'/'+inst_filename)

    else:
      if len(inst_filename) > 0:
        error_desc = 'Your file, ' + inst_filename + ', is not a supported filetype.'
      else:
        error_desc = 'Please choose a file to upload.'
      return redirect('/clustergrammer/error/'+error_desc)

  # except:
  #   print('error catch')
  #   error_desc = 'There was an error in processing your matrix. Please check your format.'
  #   return redirect('/clustergrammer/error/'+error_desc)

@app.route('/clustergrammer/matrix_upload/', methods=['POST'])
def proc_matrix_upload():
  import flask 
  import load_tsv_file
  import threading
  import time
  import StringIO

  if request.method == 'POST':

    req_file = flask.request.files['file']
    buff = StringIO.StringIO(req_file.read())

    inst_filename = req_file.filename 

    print('\ninst_filename '+inst_filename+'\n\n')

    if allowed_file(inst_filename):

      # submit placeholder to mongo 
      ###############################
      # set up database connection 
      client = MongoClient(mongo_address)
      db = client.clustergrammer

      # generate placeholder json - does not contain viz json 
      export_viz = {}
      export_viz['name'] = inst_filename
      export_viz['viz'] = 'processing'
      export_viz['dat'] = 'processing'
      export_viz['source'] = 'user_upload'

      # get the id that will be used to update the placeholder 
      viz_id = db.networks.insert( export_viz )
      viz_id = str(viz_id)

      client.close()

      # initialize thread 
      #######################
      print('initializing thread - uploading network')
      sub_function = load_tsv_file.main
      arg_list = [ buff, inst_filename, mongo_address, viz_id]
      thread = threading.Thread(target=sub_function, args=arg_list)
      thread.setDaemon(True)

      # run subprocess
      ##################
      thread.start()

      ####################
      # check subprocess 
      ####################
      max_wait_time = 15
      for wait_time in range(max_wait_time):

        # wait one second
        time.sleep(1)

        print(wait_time)
        print(thread.isAlive())

        if thread.isAlive() == False:

          print('\n\nthread is dead ... job finished\n-------------------\n')

          return 'http://amp.pharm.mssm.edu/clustergrammer/viz/'+viz_id+'/'+inst_filename

      # redirect after maximum time has elapsed 
      return 'http://amp.pharm.mssm.edu/clustergrammer/viz/'+viz_id+'/'+inst_filename

    else:

      if len(inst_filename) > 0:
        error_desc = 'Your file, ' + inst_filename + ', is not a supported filetype.'
      else:
        error_desc = 'Please choose a file to upload.'
      return error_desc

home_pages.add_routes(app)
viz_pages.add_routes(app, mongo_address)
demo_pages.add_routes(app)
enrichr_clust.add_routes(app, mongo_address)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 