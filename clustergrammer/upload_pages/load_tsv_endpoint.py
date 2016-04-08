def main(mongo_address, response_type='redirect'):
  from flask import request 
  import StringIO
  import load_tsv_file
  import threading
  import time
  
  if request.method == 'POST':

    req_file = request.files['file']
    buff = StringIO.StringIO(req_file.read())
    inst_filename = req_file.filename 

    if allowed_file(inst_filename):

      thread, viz_id = upload(mongo_address, inst_filename, buff)

      max_wait_time = 15
      for wait_time in range(max_wait_time):

        time.sleep(1)

        if thread.isAlive() == False:

          return make_response(viz_id, inst_filename, response_type=response_type)

      return make_response(viz_id, inst_filename, response_type=response_type)

    else:
      
      return upload_error()  

def allowed_file(filename):
  ALLOWED_EXTENSIONS = set(['txt', 'tsv'])
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload(mongo_address, inst_filename, buff):
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
  arg_list = [ buff, export_viz['name'], mongo_address, viz_id]
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

def make_response(viz_id, inst_filename, response_type='redirect'):
  from flask import redirect

  if response_type == 'redirect':
    return redirect('/clustergrammer/viz/'+viz_id+'/'+inst_filename)

  elif response_type == 'link':
    return 'http://amp.pharm.mssm.edu/clustergrammer/viz/'+viz_id+'/'+inst_filename