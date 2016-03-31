from flask import Blueprint, render_template, request
from flask.ext.cors import cross_origin
mongo_address = '146.203.54.165'

def add_routes(app=None):

  print('\n\n\nEnrichr_cluster\n\n\n')

  enrichr_clust = Blueprint('enrichr_clust', __name__, static_url_path='/enrichr_clust/static',
    static_folder='./static', template_folder='./templates')

  @enrichr_clust.route("/clustergrammer/Enrichr_clustergram", methods=['POST','GET'])
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
      # get enrichment data from Enrichr 
      ####################################################### 

      gmt = 'ChEA_2015'
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
      viz_url = 'http://amp.pharm.mssm.edu/clustergrammer/Enrichr/'
      qs = '?preview=false&col_order=rank&row_order=clust&N_row_sum=20'

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
      print('error making enrichr clustergram')
      error_desc = 'Error in processing Enrichr clustergram.'

      return flask.jsonify({
        'link': 'error'
      })     


  app.register_blueprint(enrichr_clust)