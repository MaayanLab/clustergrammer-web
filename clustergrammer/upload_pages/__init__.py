from flask import Blueprint, render_template, request, redirect
from flask.ext.cors import cross_origin
from pymongo import MongoClient

import Enrichr_clustergram_endpoint as enr_clust_endpoint
import vector_upload_function as vector_upload_fun
import run_load_tsv

# define allowed extension
ALLOWED_EXTENSIONS = set(['txt', 'tsv'])

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

    return vector_upload_fun.main(mongo_address)

  @upload_pages.route('/clustergrammer/upload_network/', methods=['POST'])
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

        thread, viz_id = run_load_tsv.upload(mongo_address, inst_filename, buff)

        max_wait_time = 15
        for wait_time in range(max_wait_time):

          time.sleep(1)

          if thread.isAlive() == False:

            return run_load_tsv.response(viz_id, inst_filename, response_type='redirect')

        return run_load_tsv.response(viz_id, inst_filename, response_type='redirect')

      else:
        
        return run_load_tsv.upload_error()

  @upload_pages.route('/clustergrammer/matrix_upload/', methods=['POST'])
  def proc_matrix_upload():
    import flask 
    import StringIO
    import time

    if request.method == 'POST':

      req_file = flask.request.files['file']
      buff = StringIO.StringIO(req_file.read())
      inst_filename = req_file.filename 

      if allowed_file(inst_filename):

        thread, viz_id = run_load_tsv.upload(mongo_address, inst_filename, buff)

        max_wait_time = 15
        for wait_time in range(max_wait_time):

          time.sleep(1)

          if thread.isAlive() == False:
            return run_load_tsv.response(viz_id, inst_filename, response_type='link')

        return run_load_tsv.response(viz_id, inst_filename, response_type='link')

      else:

        return run_load_tsv.upload_error()

  app.register_blueprint(upload_pages)