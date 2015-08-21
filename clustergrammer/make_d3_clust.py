
def load_file(req_file, allowed_file):

  import numpy as np
  import flask
  import make_exp_clustergram
  from pymongo import MongoClient
  from flask import request

  # set up connection 
  client = MongoClient()
  db = client.new_db

  # get the filename 
  inst_filename = req_file.filename
  
  # check that request is a post
  if request.method == 'POST' and allowed_file(inst_filename):

    # read file
    lines = req_file.readlines()

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
      inst_line = lines[i].split('\t')

      # strip each element 
      inst_line = [z.strip() for z in inst_line]

      # get column labels from first row 
      if i == 0:
        tmp_col_labels = inst_line

        # add the labels
        for inst_elem in range(len(tmp_col_labels)):

          # skip the first element 
          if inst_elem > 0:
            # get the column label 
            inst_col_label = tmp_col_labels[inst_elem]

            # ignore first element 
            network['nodes']['col'].append(inst_col_label)

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

    # run make_grammer_clustergram 
    d3_json = make_exp_clustergram.make_grammer_clustergram(network)

    # convert data_mat to list before exporting as json
    network['data_mat'] = network['data_mat'].tolist()

    # generate export dictionary 
    ###############################
    export_dict = {}
    # save name of network 
    export_dict['name'] = inst_filename
    # initial network information, including data_mat array
    export_dict['network'] = network
    # d3 json used for visualization (already clustered)
    export_dict['d3_json'] = d3_json

    # save json as new collection 
    ##################################
    db.networks.insert( export_dict )    

    # close client
    client.close()

    # return the network in json form 
    return flask.jsonify(d3_json)

  else:
    print('error in file upload - check filetype')

    return error