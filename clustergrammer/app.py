
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

# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/clustergrammer'

# address for mongodbs 
# mongo_address = '192.168.2.7'
mongo_address = '146.203.54.165'

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

# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route(ENTRY_POINT + '/<path:path>') ## original 
# @crossdomain(origin='*')
def send_static(path):
  return send_from_directory(SERVER_ROOT, path)

@app.route("/clustergrammer/")
def index():
  return render_template('index.html', flask_var='')

@app.route("/clustergrammer/error/<error_desc>")
def render_error_page(error_desc):
  return render_template('error.html', error_desc=error_desc)

@app.route("/clustergrammer/viz/<user_objid>")
def viz(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)

  gnet = db.networks.find_one({'_id': obj_id })

  client.close()

  d3_json = gnet['viz']
  viz_name = gnet['name']

  return render_template('viz.html', viz_network=d3_json, viz_name=viz_name)

@app.route("/clustergrammer/G2Egram_preview/<user_objid>")
def G2Egram_preview(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)

  gnet = db.networks.find_one({'_id': obj_id })

  client.close()
  
  d3_json = gnet['viz']
  viz_name = gnet['name']

  return render_template('G2Egram_preview.html', viz_network=d3_json, viz_name=viz_name)

@app.route("/clustergrammer/G2Egram/<user_objid>")
def G2Egram(user_objid):
  import flask
  from bson.objectid import ObjectId
  from copy import deepcopy

  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)

  gnet = db.networks.find_one({'_id': obj_id })

  client.close()
  
  d3_json = gnet['viz']
  viz_name = gnet['name']
  viz_link = gnet['link']

  return render_template('G2Egram.html', viz_network=d3_json, viz_name=viz_name, viz_link=viz_link)

@app.route("/clustergrammer/mock_l1000cds2")
def mock_l1000cds2():
  return render_template('mock_l1000cds2.html', flask_var='')

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

  print('\n\nloading from mongodb\n##################n\n')

  return render_template('l1000cds2.html', viz_network=d3_json)

@app.route('/clustergrammer/g2e/', methods=['POST'])
@cross_origin()
def proc_g2e():
  import requests 
  import flask
  import json 
  from d3_clustergram_class import Network

  # import pdb; pdb.set_trace()

  # ajax request looks like this 
  # $.ajax({
  #            url: 'g2e/',
  #            method: 'POST',
  #            contentType: 'application/json',
  #            data: JSON.stringify(tmp),
  #            success: function() {
  #                debugger;
  #            }
  #        });

  try:

    g2e_json = json.loads(request.data)

    # ini network obj 
    net = Network()

    # load g2e data into network 
    net.load_g2e_to_net(g2e_json)

    # swap nans for zeros
    net.swap_nan_for_zero()

    # filter the matrix using cutoff and min_num_meet
    ###################################################
    cutoff_meet = 0.01
    min_num_meet = 2
    net.filter_network_thresh( cutoff_meet, min_num_meet )

    # cluster 
    #############
    net.cluster_row_and_col('cos')

    # generate export dictionary 
    ###############################
    export_dict = {}
    # save name of network 
    if 'description' in g2e_json:
      export_dict['name'] = g2e_json['description']
    else:
      export_dict['name'] = 'G2Egram Results'
    # initial network information, including data_mat array
    export_dict['dat'] = net.export_net_json('dat')
    # d3 json used for visualization (already clustered)
    export_dict['viz'] = net.viz

    # save the link back to the original results
    export_dict['link'] = g2e_json['link']

    # set up connection 
    client = MongoClient(mongo_address)
    db = client.clustergrammer

    # save json as new collection 
    ##################################
    net_id = db.networks.insert( export_dict ) 

    # close client
    client.close()

    # make network a dictionary 
    gnet = {}
    gnet['viz'] = net.viz
    net_id = str(net_id)

    return flask.jsonify({
      'preview_link': 'http://amp.pharm.mssm.edu/clustergrammer/G2Egram_preview/'+net_id,
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/G2Egram/'+net_id
    })

  except:

    error_desc = 'Error in processing GEO2Enrichr signatures.'
    return flask.jsonify({
      'preview_link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc,
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
    })  


# l1000cds2 post 
############################
@app.route('/clustergrammer/l1000cds2/', methods=['POST'])
def l1000cds2_upload():

  import requests
  import json 
  from d3_clustergram_class import Network 
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
  net.cluster_row_and_col('cos', cutoff_comp, min_num_comp)  

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


# upload network 
############################
@app.route('/clustergrammer/upload_network/', methods=['POST'])
def upload_network():
  import flask 
  import load_tsv_file

  try:

    if request.method == 'POST':

      req_file = flask.request.files['file']

      inst_filename = req_file.filename 

      print('\ninst_filename '+inst_filename+'\n\n')

      if allowed_file(inst_filename):

        # cluster and add to database 
        net_id, net = load_tsv_file.main(req_file, allowed_file, mongo_address)

        print('\n\nnet_id')
        print(net_id)
        print('\n\n')

        # make network a dictionary 
        gnet = {}
        gnet['viz'] = net.viz

        return redirect('/clustergrammer/viz/'+net_id)

      else:
        if len(inst_filename) > 0:
          error_desc = 'Your file, ' + inst_filename + ', is not a supported filetype.'
        else:
          error_desc = 'Please choose file to upload.'
        return redirect('/clustergrammer/error/'+error_desc)

  except:
    print('error catch')
    error_desc = 'There was an error in processing your matrix. Please check your format.'
    return redirect('/clustergrammer/error/'+error_desc)

# CST 
##############
@app.route('/clustergrammer/cstgram/', methods=['GET'])
def cstgram_home():

  return render_template('cstgram_home.html', flask_var='')

@app.route('/clustergrammer/cstgram_data/', methods=['POST'])
def cstgram_data():
  import json

  # $.post( "cstgram_data/", {name:'nick'}).done(function(data){console.log(data)});

  # post request on front end 
  ###############################
  # $.ajax({
  #           url: 'cstgram_data/',
  #           type: 'post',
  #           dataType: 'json',
  #           success: function (data) {
  #               console.log('here');
  #           },
  #           data: JSON.stringify(person)
  #       });

  if request.method == 'POST':
    req_json = json.loads(request.get_data())

    print(type(req_json))
    print(req_json)

    return 'some response from the server!!!'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 