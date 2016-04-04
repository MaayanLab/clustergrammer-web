from flask import Blueprint, render_template, request
from flask.ext.cors import cross_origin
import flask 
import json 
from pymongo import MongoClient
import threading 
import time 

import run_enrich_background as enr_sub
import enrichr_functions as enr_fun

import fake_enrichr 

def add_routes(app=None, mongo_address=None):

  print('\n\n\nEnrichr_cluster\n\n\n')

  enrichr_clust = Blueprint('enrichr_clust', __name__, 
    static_url_path='/enrichr_clust/static', static_folder='./static', 
    template_folder='./templates')

  @enrichr_clust.route("/clustergrammer/Enrichr_clustergram", methods=['POST','GET'])
  @cross_origin()
  def enrichr_clustergram():

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

        if thread.isAlive() == False:

          return flask.jsonify({'link': viz_url+viz_id+qs})

      # return link after max time has elapsed 
      return flask.jsonify({'link': viz_url+viz_id+qs})

    except:
      error_desc = 'Error in processing Enrichr clustergram.'

      return flask.jsonify({
        'link': 'error'
      })     

  app.register_blueprint(enrichr_clust)