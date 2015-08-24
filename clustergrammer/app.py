
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import send_from_directory

# import mongo related things 
# method from donorschoose not working 
# from pymongo import Connection
# method from python_mongo_tutorial
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
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/clustergrammer/clustergrammer' ## original 

# # for docker development
# SERVER_ROOT = '/app/clustergrammer'


# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route(ENTRY_POINT + '/<path:path>') ## original 
# @crossdomain(origin='*')
def send_static(path):
  return send_from_directory(SERVER_ROOT, path)


# @app.route("/clustergrammer/<tmp>")
@app.route("/clustergrammer/")
# def index(tmp):
def index():
  # print(tmp)
  print('Rendering index template')
  return render_template('index.html', flask_var='')


@app.route("/clustergrammer/viz/<user_objid>")
def viz(user_objid):
  import flask
  from bson.objectid import ObjectId

  # 55d945129ff08807f604278b - from_excel.txt
  # 55d945529ff08807f604278c

  print(user_objid)
  # set up connection 
  client = MongoClient()
  db = client.clustergrammer

  # make query for data with name 'from_excel.txt'
  cursor = db.networks.find_one({'_id': ObjectId(user_objid) })

  print('name')
  print(cursor['name'])
  print(cursor['viz'])

  # close connection 
  client.close()

  print('Rendering viz template')
  return render_template('viz.html', viz_network=cursor['viz'])


# load previous result route 
@app.route('/clustergrammer/load_saved/', methods=['GET'])
def load_saved():
  import flask

  # set up connection 
  client = MongoClient()
  db = client.clustergrammer

  # get filename 
  querystring = request.args
  querystring = dict(querystring)
  load_filename = querystring['id'][0]

  # make query for data with name 'from_excel.txt'
  cursor = db.networks.find_one({'name':load_filename})

  print('name')
  print(cursor['name'])

  # close connection 
  client.close()

  # return flask.jsonify( cursor['d3_json'] ) 

  clustergram_id= 'some-clustergram-id'
  print(clustergram_id)
  print('\n\n\n')
  return render_template('index.html', flask_var='loading saved data')
  # return redirect('/clustergrammer/redirected_url/')

# Jquery upload file route 
############################
@app.route('/clustergrammer/jquery_upload/', methods=['GET','POST'])
def jquery_upload_function():
  import flask 
  import d3_clustergram
  import make_d3_clust

  # # don't know if I need this 
  # error = None 

  req_file = flask.request.files['file']

  # add to database 

  # return visualization json 
  # d3_json = make_d3_clust.load_file( req_file, allowed_file )

  # # return net class 
  # net = make_d3_clust.load_file(req_file, allowed_file)

  # return net_id only 
  net_id = make_d3_clust.load_file(req_file, allowed_file)

  # redirect to vi
  print('\n\n\n')
  print(net_id)
  print(type(net_id))
  return redirect('/clustergrammer/viz/'+str(net_id))


  # return d3_json






if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 