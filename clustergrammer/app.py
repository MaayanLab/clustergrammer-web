
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

# # local
# mongo_address = '10.125.168.181'

# lab 
mongo_address = '146.203.54.165'

##########################################
# switch for local and docker development 
# docker_vs_local
##########################################

# # for local development 
# SERVER_ROOT = os.path.dirname(os.getcwd()) + '/clustergrammer/clustergrammer' 

# for docker development
SERVER_ROOT = '/app/clustergrammer'
# change routing of logs when running docker 
logging.basicConfig(stream=sys.stderr) 

######################################

# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route(ENTRY_POINT + '/<path:path>') 
def send_static(path):
  return send_from_directory(SERVER_ROOT, path)

@app.route("/clustergrammer/")
@app.route("/Clustergrammer/")
@app.route("/CLUSTERGRAMMER/")
def index():
  return render_template('index.html', flask_var='')

@app.route("/clustergrammer/help")
def help():
  return render_template('help.html')  


@app.route("/clustergrammer/error/<error_desc>")
def render_error_page(error_desc):
  return render_template('error.html', error_desc=error_desc)

@app.route("/clustergrammer/viz/<user_objid>")
@app.route("/clustergrammer/viz/<user_objid>/<slug>")
def viz(user_objid, slug=None):
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

@app.route("/clustergrammer/demo/<user_objid>")
def demo(user_objid):
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

  return render_template('demo.html', viz_network=d3_json, viz_name=viz_name)  

@app.route("/clustergrammer/load_Enrichr_gene_lists", methods=['POST','GET'])
@cross_origin()
def enrichment_vectors():
  import requests 
  import flask 
  import json 
  from pymongo import MongoClient
  import threading 
  import time 
  import run_enrich_background as enr_sub

  if request.method == 'POST':
    g2e_post = json.loads(request.data)

  elif request.method == 'GET':

    ####################################################### 
    # mock data 
    ####################################################### 
    g2e_post = {
      "viz_title":"Aging-Study",
      "background_type": "KEA_2015",
      "signature_ids": [
        {
          "enr_id_up": "949840",
          "col_title": "Age effect on lipopolysaccharide-induced neuroinflammation and sickness behavior",
          "enr_id_dn": "949841"
        },
        {
          "enr_id_up": "949842",
          "col_title": "Age effect on lipopolysaccharide-induced neuroinflammation and sickness behavior 2",
          "enr_id_dn": "949843"
        },
        {
          "enr_id_up": "949844",
          "col_title": "Age effect on extraocular muscles",
          "enr_id_dn": "949845"
        },
        {
          "enr_id_up": "949846",
          "col_title": "Age effect on extraocular muscles 2",
          "enr_id_dn": "949847"
        }
      ]
    }


    ####################################################### 
    ####################################################### 

    print('\n\nGET: running mock enrichment through get request')

  try:  

    # submit placeholder to mongo 
    ################################

    # set up database connection 
    client = MongoClient(mongo_address)
    db = client.clustergrammer

    # generate placeholder json - does not contain viz json 
    export_viz = {}
    if 'viz_title' in g2e_post:
      export_viz['name'] = g2e_post['viz_title']
    else:
      export_viz['name'] = 'enrichment_vector'
    export_viz['viz'] = 'processing'
    export_viz['dat'] = 'processing'
    export_viz['source'] = 'g2e_enr_vect'

    # this is the id that will be used to view the visualization 
    viz_id = db.networks.insert( export_viz )
    viz_id = str(viz_id)

    # close database connection 
    client.close()
    
    # initialize thread
    ######################
    sub_function = enr_sub.make_enr_vect_clust
    arg_list = [mongo_address, viz_id, g2e_post]
    thread = threading.Thread(target=sub_function, args=arg_list)
    thread.setDaemon(True)

    # run subprocess 
    ####################
    print('\n\n----------------------------------------------------')
    print(export_viz['name'] + ': Starting enr_vect_clust subprocess: ' )
    print('----------------------------------------------------\n')
    thread.start()

    # define information return link - always the same link 
    ######################################
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
        
        return flask.jsonify({'link': viz_url+viz_id+inst_name})

    # return link after max time has elapsed 
    return flask.jsonify({'link': viz_url+viz_id+inst_name})

  except:
    error_desc = 'Error in processing Enrichr enrichment vectors.'

    return flask.jsonify({
      'link': 'http://amp.pharm.mssm.edu/clustergrammer/error/'+error_desc
    }) 

@app.route("/clustergrammer/Enrichr_clustergram", methods=['POST','GET'])
@cross_origin()
def enrichr_clustergram():
  import requests 
  import flask 
  import json 
  from pymongo import MongoClient
  import threading 
  import time 
  import run_enrich_background as enr_sub
  import enrichr_functions as enr_fun

  if request.method == 'POST':
    enr_json = json.loads(request.data)

  elif request.method == 'GET':

    ####################################################### 
    # mock data 
    ####################################################### 

    gmt = 'KEA_2015'
    userListId = 939279

    # define the get url 
    get_url = 'http://amp.pharm.mssm.edu/Enrichr/enrich'

    # get parameters 
    params = {'backgroundType':gmt,'userListId':userListId}

    # try get request until status code is 200 
    inst_status_code = 400

    # wait until okay status code is returned 
    num_try = 0
    while inst_status_code == 400 and num_try < 100:
      num_try = num_try +1 
      try:
        # make the get request to get the enrichr results 
        print('make-get-req-Enrichr')

        try:
          get_response = requests.get( get_url, params=params )

          # get status_code
          inst_status_code = get_response.status_code
          print('inst_status_code: '+str(inst_status_code))

        except:
          print('get request failed\n------------------------\n\n')

      except:
        pass

    # load as dictionary 
    resp_json = json.loads( get_response.text )

    # get the key 
    only_key = resp_json.keys()[0]

    # get response_list 
    response_list = resp_json[only_key]

    enr_json = {}
    enr_json['userListId'] = userListId
    enr_json['gmt'] = gmt
    enr_json['enr_list'] = response_list


    ####################################################### 
    ####################################################### 

    print('\n\nrunning mock enrichment through get request\n\n')

  try:  

    print('making clust')

    # submit placeholder to mongo 
    ################################

    # set up database connection 
    client = MongoClient(mongo_address)
    db = client.clustergrammer

    # generate placeholder json - does not contain viz json 
    export_viz = {}
    export_viz['name'] = str(enr_json['userListId']) + '_' + enr_json['gmt']
    export_viz['viz'] = 'processing'
    export_viz['dat'] = 'processing'
    export_viz['source'] = 'Enrichr_clustergram'

    # this is the id that will be used to view the visualization 
    viz_id = db.networks.insert( export_viz )
    viz_id = str(viz_id)

    # close database connection 
    client.close()
    
    # initialize thread
    ######################
    print('initializing thread')
    sub_function = enr_sub.Enrichr_cluster
    arg_list = [mongo_address, viz_id, enr_json['enr_list']]
    thread = threading.Thread(target=sub_function, args=arg_list)
    thread.setDaemon(True)

    # run subprocess 
    ####################
    print('running subprocess and pass in viz_id ')
    thread.start()

    # define information return link - always the same link 
    ######################################
    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'
    qs = '?preview=true&order=rank&viz_type=Enrichr_clustergram'

    # check if subprocess is finished 
    ###################################
    max_wait_time = 30
    print('check if subprocess is done')
    for wait_time in range(max_wait_time):

      # wait one second 
      time.sleep(1)

      print('wait_time'+str(wait_time)+' '+str(thread.isAlive()))

      if thread.isAlive() == False:

        print('\n\nthread is dead\n----------\n')
        
        return flask.jsonify({'link': viz_url+viz_id+qs})

    # return link after max time has elapsed 
    return flask.jsonify({'link': viz_url+viz_id+qs})

  except:
    print('here')
    error_desc = 'Error in processing Enrichr clustergram.'

    return flask.jsonify({
      'link': 'error'
    })   


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

  print('\n\nloading from mongodb\n##################n\n')

  return render_template('l1000cds2.html', viz_network=d3_json)

@app.route('/clustergrammer/g2e/', methods=['POST','GET'])
@cross_origin()
def proc_g2e():
  import requests 
  import flask
  import json 
  from clustergrammer import Network

  # ini network obj 
  net = Network()

  if request.method == 'POST':
    g2e_json = json.loads(request.data)

  elif request.method == 'GET':
    g2e_json = net.load_json_to_dict('clustergrammer/mock_g2e.json')


  try:

    # load g2e data into network 
    net.load_g2e_to_net(g2e_json)

    # swap nans for zeros
    net.swap_nan_for_zero()

    # cluster g2e using pandas
    net.fast_mult_views()

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
    # save source 
    export_dict['source'] = 'g2e'

    # # save the link back to the original results
    # export_dict['link'] = g2e_json['link']

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

    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/viz/'

    col_label = 'G2E Signatures'
    row_label = 'genes'
    qs = 'col_label='+col_label+'&'+'row_label='+row_label

    return flask.jsonify({
      'preview_link': viz_url+net_id+'?preview=true&'+qs,
      'link': viz_url+net_id+'?'+qs
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
  import threading
  import time
  import StringIO

  # try:

  if request.method == 'POST':

    req_file = flask.request.files['file']
    buff = StringIO.StringIO(req_file.read())

    inst_filename = req_file.filename 

    print('\ninst_filename '+inst_filename+'\n\n')

    if allowed_file(inst_filename):

      print('allowed file')

      # # cluster and add to database 
      # net_id, inst_filename = load_tsv_file.main(req_file, allowed_file, mongo_address)

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

      # get the id that will be used to view the visualization 
      viz_id = db.networks.insert( export_viz )
      viz_id = str(viz_id)

      client.close()

      # initialize thread 
      #######################
      print('initializing thread')
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

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 