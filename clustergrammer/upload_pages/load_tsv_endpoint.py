def main(mongo_address, response_type='redirect', req_sim_mat=False):
  from flask import request
  import StringIO
  import threading
  import time

  if request.method == 'POST':

    # set values for distance and linkage types
    #############################################
    if 'distance-type' in request.values:
      distance_type = request.values['distance-type']
    else:
      distance_type = 'cosine'

    if 'linkage-type' in request.values:
      linkage_type = request.values['linkage-type']
    else:
      linkage_type = 'average'

    req_file = request.files['file']
    buff = StringIO.StringIO(req_file.read())
    inst_filename = req_file.filename

    if allowed_file(inst_filename):

      thread, viz_id = start_upload(mongo_address, inst_filename, buff,
                                    req_sim_mat, distance_type, linkage_type)

      max_wait_time = 45
      for wait_time in range(max_wait_time):

        time.sleep(1)

        if thread.isAlive() == False:

          return make_response(viz_id, inst_filename, response_type=response_type, req_sim_mat=req_sim_mat)

      return make_response(viz_id, inst_filename, response_type=response_type, req_sim_mat=req_sim_mat)

    else:

      return upload_error(inst_filename)

def allowed_file(filename):
  ALLOWED_EXTENSIONS = set(['txt', 'tsv'])
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def start_upload(mongo_address, inst_filename, buff, req_sim_mat=False,
                 distance_type='cosine', linkage_type='average'):

  from pymongo import MongoClient
  import threading
  import load_tsv_file

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
  arg_list = [ buff, export_viz['name'], mongo_address, viz_id, req_sim_mat,
               distance_type, linkage_type]
  thread = threading.Thread(target=sub_function, args=arg_list)
  thread.setDaemon(True)

  thread.start()

  return thread, viz_id

def upload_error(inst_filename):

  if len(inst_filename) > 0:
    error_desc = 'Your file, ' + inst_filename + ', is not a supported filetype.'
  else:
    error_desc = 'Please choose a file to upload.'

  return error_desc

def make_response(viz_id, inst_filename, response_type='redirect', req_sim_mat=False):
  from flask import redirect, current_app

  if response_type == 'redirect':
    if req_sim_mat:
      inst_redirect = redirect(current_app.config['ENTRY_POINT'] + '/viz_sim_mats/'+viz_id+'/'+inst_filename)
    else:
      inst_redirect = redirect(current_app.config['ENTRY_POINT'] + '/viz/'+viz_id+'/'+inst_filename)
    return inst_redirect

  elif response_type == 'link':
    if req_sim_mat:
      inst_link = current_app.config['ORIGIN'] + current_app.config['ENTRY_POINT'] + '/viz_sim_mats/'+viz_id+'/'+inst_filename
    else:
      inst_link = current_app.config['ORIGIN'] + current_app.config['ENTRY_POINT'] + '/viz/'+viz_id+'/'+inst_filename

    return inst_link
