def main(mongo_address, inst_filename, buff):
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