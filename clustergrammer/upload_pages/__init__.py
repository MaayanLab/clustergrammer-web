from flask import Blueprint, render_template, request, redirect
from flask.ext.cors import cross_origin
from pymongo import MongoClient

import Enrichr_clustergram_endpoint as enr_clust_endpoint
import vector_upload_function as vector_upload_fun

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

  app.register_blueprint(upload_pages)