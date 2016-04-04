def main(mongo_address):
  import json 
  import fake_enrichr 
  from pymongo import MongoClient
  import threading 
  import flask 
  import time 
  import run_enrich_background as enr_sub
  from flask import request

  if request.method == 'POST':
    enr_json = json.loads(request.data)

  elif request.method == 'GET':

    enr_json = fake_enrichr.fake_post()   

  try:  

    client = MongoClient(mongo_address)
    db = client.clustergrammer

    export_viz = {}
    export_viz['name'] = str(enr_json['userListId']) + '_' + enr_json['gmt']
    export_viz['viz'] = 'processing'
    export_viz['dat'] = 'processing'
    export_viz['source'] = 'Enrichr_clustergram'

    viz_id = db.networks.insert( export_viz )
    viz_id = str(viz_id)

    client.close()
    
    sub_function = enr_sub.Enrichr_cluster
    arg_list = [mongo_address, viz_id, enr_json['enr_list']]
    thread = threading.Thread(target=sub_function, args=arg_list)
    thread.setDaemon(True)

    thread.start()

    viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/Enrichr_new/'
    qs = '?preview=false&col_order=rank&row_order=clust&N_row_sum=20'

    max_wait_time = 30
    for wait_time in range(max_wait_time):

      # wait one second 
      time.sleep(1)

      print('wait time ' + str(wait_time) )

      if thread.isAlive() == False:

        print('thread is done')

        return flask.jsonify({'link': viz_url+viz_id+qs})

    return flask.jsonify({'link': viz_url+viz_id+qs})

  except:
    error_desc = 'Error in processing Enrichr clustergram.'

    return flask.jsonify({
      'link': 'error'
    })     

