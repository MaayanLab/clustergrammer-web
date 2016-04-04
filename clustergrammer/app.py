
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
import upload_pages
import status_check

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/clustergrammer'

# address for mongodbs 

# # local
# mongo_address = '192.168.1.2'

# lab 
mongo_address = '146.203.54.165'

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

@app.route('/clustergrammer/l1000cds2/', methods=['POST'])
def l1000cds2_upload():
  import requests
  import json 
  from clustergrammer import Network 
  from pymongo import MongoClient
  from bson.objectid import ObjectId

  l1000cds2 = json.loads( request.form.get('signatures') )

  net = Network()

  net.load_l1000cds2(l1000cds2)

  cutoff_comp = 0
  min_num_comp = 2
  net.cluster_row_and_col(dist_type='cosine', dendro=True)  

  net.dat['node_info']['row']['ini'] = net.sort_rank_node_values('row')
  net.dat['node_info']['col']['ini'] = net.sort_rank_node_values('col')
  net.viz = {}
  net.viz['row_nodes'] = []
  net.viz['col_nodes'] = []
  net.viz['links'] = []
  net.viz_json()

  export_dict = {}
  export_dict['name'] = 'l1000cds2'
  export_dict['dat'] = net.export_net_json('dat')
  export_dict['viz'] = net.viz
  export_dict['_id'] = ObjectId(l1000cds2['_id'])
 
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  tmp = db.networks.find_one({'_id': ObjectId(l1000cds2['_id']) })
  if tmp is None:
    tmp_id = db.networks.insert( export_dict ) 

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

    if allowed_file(inst_filename):

      client = MongoClient(mongo_address)
      db = client.clustergrammer

      export_viz = {}
      export_viz['name'] = inst_filename
      export_viz['viz'] = 'processing'
      export_viz['dat'] = 'processing'
      export_viz['source'] = 'user_upload'

      viz_id = db.networks.insert( export_viz )
      viz_id = str(viz_id)

      client.close()

      sub_function = load_tsv_file.main
      arg_list = [ buff, inst_filename, mongo_address, viz_id]
      thread = threading.Thread(target=sub_function, args=arg_list)
      thread.setDaemon(True)

      thread.start()

      max_wait_time = 15
      for wait_time in range(max_wait_time):

        # wait one second
        time.sleep(1)

        if thread.isAlive() == False:

          return redirect('/clustergrammer/viz/'+viz_id+'/'+inst_filename)

      return redirect('/clustergrammer/viz/'+viz_id+'/'+inst_filename)

    else:
      if len(inst_filename) > 0:
        error_desc = 'Your file, ' + inst_filename + ', is not a supported filetype.'
      else:
        error_desc = 'Please choose a file to upload.'
      return redirect('/clustergrammer/error/'+error_desc)

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

    if allowed_file(inst_filename):

      client = MongoClient(mongo_address)
      db = client.clustergrammer

      export_viz = {}
      export_viz['name'] = inst_filename
      export_viz['viz'] = 'processing'
      export_viz['dat'] = 'processing'
      export_viz['source'] = 'user_upload'

      # get the id that will be used to update the placeholder 
      viz_id = db.networks.insert( export_viz )
      viz_id = str(viz_id)

      client.close()

      sub_function = load_tsv_file.main
      arg_list = [ buff, inst_filename, mongo_address, viz_id]
      thread = threading.Thread(target=sub_function, args=arg_list)
      thread.setDaemon(True)

      thread.start()

      max_wait_time = 15
      for wait_time in range(max_wait_time):

        time.sleep(1)

        if thread.isAlive() == False:
          return 'http://amp.pharm.mssm.edu/clustergrammer/viz/'+viz_id+'/'+inst_filename

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
upload_pages.add_routes(app, mongo_address)
status_check.add_routes(app, mongo_address)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 