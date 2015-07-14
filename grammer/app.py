
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import json
import sys
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import send_from_directory

# # change routing of logs when running docker 
# logging.basicConfig(stream=sys.stderr) 



# app = Flask(__name__)
app = Flask(__name__, static_url_path='')

ENTRY_POINT = '/grammer'

# switch for local and docker development 
# docker_vs_local
##########################################

# for local development 
SERVER_ROOT = os.path.dirname(os.getcwd()) + '/grammer/grammer' ## original 

# # for docker development
# SERVER_ROOT = '/app/grammer'


@app.route(ENTRY_POINT + '/<path:path>') ## original 
# @crossdomain(origin='*')
def send_static(path):

  # print('path and SERVER_ROOT')
  # print(path)
  # print(SERVER_ROOT)
  
  return send_from_directory(SERVER_ROOT, path)


@app.route("/grammer/")
def index():
  print('Rendering index template')
  return render_template("index.html")

# post request
@app.route('/grammer/', methods=['GET','POST'])
def python_function():
  import flask 
  # import make_enr_clust
  import make_exp_clustergram
  import json 
  import json_scripts 
  import sys
  import cookielib, poster, urllib2, json

  error = None 

  # get request json 
  req_json = request.form

  # get the gene class 
  inst_name = req_json['name'] # request.form['name'].upper()

  # generate an expression clustergram using cst code 
  d3_json = make_exp_clustergram.tf_clust(inst_name)

  # jsonify network 
  #####################
  return flask.jsonify(d3_json)



# Jquery upload file 
############################
@app.route('/jquery_upload/', methods=['GET','POST'])
def jquery_upload_function():
  import flask 
  import make_exp_clustergram
  import d3_clustergram
  import numpy as np
  
  # # don't know if I need this 
  # error = None 

  # python dbeugger
  ####################
  # import pdb; pdb.set_trace()
  
  if request.method == 'POST':

    # read file
    lines = flask.request.files['file'].readlines()

    # initialize dictionary 
    #############################
    network = {}
    network['nodes'] = {}
    network['nodes']['row'] = []
    network['nodes']['col'] = []

    # get the row and column labels and data from lines 
    #####################################################
    for i in range(len(lines)):

      # get inst_line
      inst_line = lines[i].strip().split('\t')

      # get column labels from first row 
      if i == 0:
        tmp_col_labels = inst_line

        # add the labels
        for inst_col in tmp_col_labels:
          # ignore blank labels (may not occur)
          if inst_col != '':
            network['nodes']['col'].append(inst_col)

      # get row labels 
      if i > 0:

        # save row labels 
        network['nodes']['row'].append(inst_line[0])

        # get data (still strings)
        inst_data_row = inst_line[1:]

        # convert strings to floats 
        inst_data_row = [float(x) for x in inst_data_row]

        # save the row data as an arry 
        inst_data_row =  np.asarray(inst_data_row) 

        # initialize the matrix 
        if i == 1:
          network['data_mat'] = inst_data_row

        # add rows to matrix
        if i > 1:
          network['data_mat'] = np.vstack( (network['data_mat'], inst_data_row) )

    # check status of matrix   
    print(network['data_mat'])

    # # convert data_mat to list before exporting as json
    # network['data_mat'] = network['data_mat'].tolist()

    # run make_grammer_clustergram 
    d3_json = make_exp_clustergram.make_grammer_clustergram(network)

    # return the network in json form 
    return flask.jsonify(d3_json)

  # return an error if the request is not a post 
  else:
    return 'erorr'



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
 