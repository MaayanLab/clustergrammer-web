
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

# # change routing of logs when running docker 
# logging.basicConfig(stream=sys.stderr) 

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/clustergrammer'

# switch for local and docker development 
# docker_vs_local
##########################################

# for local development 
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/clustergrammer/clustergrammer' 

# # for docker development
# SERVER_ROOT = '/app/clustergrammer'

######################################

# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])
# define global network 
gnet = []
gnet_id = []

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route(ENTRY_POINT + '/<path:path>') ## original 
# @crossdomain(origin='*')
def send_static(path):
  return send_from_directory(SERVER_ROOT, path)


@app.route("/clustergrammer/")
def index():
  return render_template('index.html', flask_var='')

@app.route("/clustergrammer/mock_l1000cds2")
def mock_l1000cds2():
  return render_template('mock_l1000cds2.html', flask_var='')

@app.route("/clustergrammer/viz/<user_objid>")
def viz(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  # example mongodb ids 
  # 55d945129ff08807f604278b - from_excel.txt
  # 55d945529ff08807f604278c - med ccle
  # 55f2458f9ff088ccfd32a805 - large ccle

  global gnet_id
  global gnet

  if gnet_id == user_objid and type(gnet) is not list:

    # use preloaded network 
    print('\n\nusing global network\n##################n\n')
    d3_json = deepcopy(gnet['viz'])

  else:

    # set up connection 
    # client = MongoClient('146.203.54.165')
    client = MongoClient()
    db = client.clustergrammer
    # make query for data with name 'from_excel.txt'
    gnet = db.networks.find_one({'_id': ObjectId(user_objid) })

    # close connection 
    client.close()
    d3_json = gnet['viz']
    gnet_id = deepcopy(user_objid)

    print('\n\nloading from mongodb\n##################n\n')

  return render_template('viz.html', viz_network=d3_json)

@app.route("/clustergrammer/l1000cds2/<user_objid>")
def viz_l1000cds2(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  # example mongodb ids 
  # 55d945129ff08807f604278b - from_excel.txt
  # 55d945529ff08807f604278c - med ccle
  # 55f2458f9ff088ccfd32a805 - large ccle

  global gnet_id
  global gnet

  if gnet_id == user_objid and type(gnet) is not list:

    # use preloaded network 
    print('\n\nusing global network\n##################n\n')
    d3_json = deepcopy(gnet['viz'])

  else:

    # set up connection 
    # client = MongoClient('146.203.54.165')
    client = MongoClient()
    db = client.clustergrammer
    # make query for data with name 'from_excel.txt'

    gnet = db.networks.find_one({'_id': ObjectId(user_objid) })

    # close connection 
    client.close()
    print('\n\nuser_objid')
    print(user_objid)
    print('\n\n')
    d3_json = gnet['viz']
    gnet_id = deepcopy(user_objid)

    print('\n\nloading from mongodb\n##################n\n')

  return render_template('l1000cds2.html', viz_network=d3_json)

@app.route('/clustergrammer/g2e/', methods=['POST'])
def proc_g2e():
  import requests 
  import json 
  from d3_clustergram_class import Network

  global gnet_id
  global gnet

  if request.method == 'POST':
    g2e_json = json.loads( request.data )

    print('\n\n')
    print(g2e_json.keys())
    print(type(g2e_json))

    # ini network obj 
    net = Network()

    # load g2e data into network 
    net.load_g2e_to_net(g2e_json)

    # swap nans for zeros
    net.swap_nan_for_zero()

    # filter the matrix using cutoff and min_num_meet
    ###################################################
    cutoff_meet = 0.5
    min_num_meet = 10
    net.filter_network_thresh( cutoff_meet, min_num_meet )

    # cluster 
    #############
    cutoff_comp = 0.25
    min_num_comp = 3  
    net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)

    # generate export dictionary 
    ###############################
    export_dict = {}
    # save name of network 
    export_dict['name'] = 'tmp'
    # initial network information, including data_mat array
    export_dict['dat'] = net.export_net_json('dat')
    # d3 json used for visualization (already clustered)
    export_dict['viz'] = net.export_net_json('viz')

    # set up connection 
    # client = MongoClient('146.203.54.165')
    client = MongoClient()
    db = client.clustergrammer

    # save json as new collection 
    ##################################
    print('loading data to matrix')
    net_id = db.networks.insert( export_dict ) 

    # close client
    client.close()

    # make network a dictionary 
    gnet = {}
    gnet['viz'] = net.viz
    net_id = str(net_id)
    gnet_id = net_id

    # redirect to viz layout 
    print('redirecting to viz')
    return redirect('/clustergrammer/viz/'+net_id)

  else:

    client.close()

    return error 


# l1000cds2 post 
############################
@app.route('/clustergrammer/l1000cds2/', methods=['POST'])
def l1000cds2_upload():
  import requests
  import d3_clustergram
  import make_d3_clust
  import json 
  from d3_clustergram_class import Network 
  from pymongo import MongoClient
  from bson.objectid import ObjectId

  print('\n\n\n\n\n')
  print('in l1000cds2_upload')
  print('recieving a post request')

  # get data from file 
  print('read the file ')
  req_file = request.files['file']

  # read in the json from the file 
  l1000cds2 = json.loads( req_file.read() ) 

  # initialize network 
  net = Network()

  # check the keys in l1000cds2
  print(l1000cds2.keys())

  print('load network, cluster, get visualization, and redirect to viz')  

  # load l1000cds2 to .dat 
  net.load_l1000cds2(l1000cds2)

  # cluster 
  cutoff_comp = 1
  min_num_comp = 2
  net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)  

  # generate export dictionary 
  ###############################
  export_dict = {}
  # save name of network 
  export_dict['name'] = 'tmp'
  # initial network information, including data_mat array
  #!! need to convert arrays to lists in .dat 
  export_dict['dat'] = net.export_net_json('dat')
  # d3 json used for visualization (already clustered)
  export_dict['viz'] = net.viz
  export_dict['_id'] = ObjectId(l1000cds2['_id'])
  # print(l1000cds2['_id'])
 
  # set up connection 
  # client = MongoClient('146.203.54.165')
  client = MongoClient()
  db = client.clustergrammer

  # save json as new collection 
  ##################################
  print('loading data to matrix')
  tmp = db.networks.find_one({'_id': ObjectId(l1000cds2['_id']) })
  if tmp is None:
    tmp_id = db.networks.insert( export_dict ) 

  # close client
  client.close()

  print('\n\n\n\n\n')

  return redirect('/clustergrammer/l1000cds2/'+l1000cds2['_id'])


# Jquery upload file route 
############################
@app.route('/clustergrammer/jquery_upload/', methods=['POST'])
def jquery_upload_function():
  import flask 
  import d3_clustergram
  import make_d3_clust

  # # don't know if I need this 
  # error = None 

  if request.method == 'POST':
    req_file = flask.request.files['file']

    global gnet
    global gnet_id

    # cluster and add to database 
    net_id, net = make_d3_clust.load_file(req_file, allowed_file)

    # make network a dictionary 
    gnet = {}
    gnet['viz'] = net.viz
    gnet_id = net_id

    # redirect to viz layout 
    print('redirecting to viz')
    return redirect('/clustergrammer/viz/'+net_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 