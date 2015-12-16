# define a class for networks 
class Network(object):
  '''
  Networks have two states: the data state where they are stored as: matrix and nodes; 
  and a viz state where they are stored as: viz.links, viz.row_nodes, viz.col_nodes.

  The goal is to start in a data-state and produce a viz-state of the network that will be 
  used as input to clustergram.js.
  '''

  def __init__(self):
    # network: data-state
    self.dat = {}
    self.dat['nodes'] = {}
    self.dat['nodes']['row'] = []
    self.dat['nodes']['col'] = []

    # node_info holds the orderings (ini, clust, rank), classification ('cl'), and other general information 
    self.dat['node_info'] = {}
    for inst_rc in self.dat['nodes']:
      self.dat['node_info'][inst_rc] = {}
      self.dat['node_info'][inst_rc]['ini'] = []
      self.dat['node_info'][inst_rc]['clust'] = []
      self.dat['node_info'][inst_rc]['rank'] = []
      self.dat['node_info'][inst_rc]['info'] = []
      # classification is specifically used to color the class triangles 
      self.dat['node_info'][inst_rc]['cl'] = []
      self.dat['node_info'][inst_rc]['value'] = []

    # initialize matrix 
    self.dat['mat'] = []
    # mat_info is an optional dictionary 
    # so I'm not including it by default 

    # network: viz-state
    self.viz = {}
    self.viz['row_nodes'] = []
    self.viz['col_nodes'] = []
    self.viz['links'] = []

  def load_tsv_to_net(self, filename):

    f = open(filename,'r')
    lines = f.readlines()
    f.close()

    self.load_lines_from_tsv_to_net(lines)

  def pandas_load_tsv_to_net(self, filename):
    import pandas as pd 

    tmp_df = pd.read_table(filename, index_col=0)

    # save to self
    tmp_dat = self.df_to_dat(tmp_df)

    self.dat['nodes'] = tmp_dat['nodes']
    self.dat['mat'] = tmp_dat['mat']


  def load_lines_from_tsv_to_net(self, lines):
    import numpy as np
    # get row/col labels and data from lines 
    for i in range(len(lines)):

      # get inst_line
      inst_line = lines[i].rstrip().split('\t')
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

            # add to network data 
            self.dat['nodes']['col'].append(inst_col_label)

      # get row info 
      if i > 0:

        # save row labels 
        self.dat['nodes']['row'].append(inst_line[0])

        # get data - still strings 
        inst_data_row = inst_line[1:]

        # convert to float
        inst_data_row = [float(tmp_dat) for tmp_dat in inst_data_row]

        # save the row data as an array 
        inst_data_row = np.asarray(inst_data_row)

        # initailize matrix 
        if i == 1:
          self.dat['mat'] = inst_data_row

        # add rows to matrix
        if i > 1: 
          self.dat['mat'] = np.vstack( ( self.dat['mat'], inst_data_row ) )

  def load_hgram(self, filename, max_num_links=50000):
    import numpy as np

    # example data format 
    ###########################
    #   # # DatasetName Achilles Cell Line Gene Essentiality Profiles
    #   # # DatasetGroup  disease or phenotype associations
    #   GeneSym NA  NA/DatasetID  1
    #   1060P11.3 na  na  0
    #   3.8-1.2 na  na  0
    #   3.8-1.5 na  na  0
    #   A1BG  na  na  0
    #   A1BG-AS1  na  na  0
    #   A1CF  na  na  0
    #   A2M na  na  0 

    # processing steps
    # line 1 has dataset names starting on 4th column 
    # line 2 has dataset groups starting on 4th column 
    # line 3 has column labels and dataset numbers, but no information that I need
    # line 4 and after have gene symbols (first column) and values (4th and after columns)

    # # load gene classes for harmonogram 
    # gc = self.load_json_to_dict('gene_classes_harmonogram.json')

    f = open(filename,'r')
    lines = f.readlines()
    f.close()

    # loop through the lines of the file 
    for i in range(len(lines)):

      # get the inst_line and make list 
      inst_line = lines[i].strip().split('\t')

      # line 1: get dataset names 
      if i ==0:

        # gather column information 
        for j in range(len(inst_line)):
          # skip the first three columns
          if j > 2: 
            # get inst label
            inst_col = inst_line[j]
            # gather column labels 
            self.dat['nodes']['col'].append(inst_col)

      # line 2: get dataset groups - do not save as 'cl', save as 'info' to sidestep clustergram.js code
      if i ==1:
        # gather column classification information 
        for j in range(len(inst_line)):
          # skip the first three columns
          if j > 2: 
            # get inst label
            inst_col = inst_line[j]
            # gather column labels 
            self.dat['node_info']['col']['info'].append(inst_col)

      # line 3: no information 

      # line 4: get gene symbol and data 
      if i > 2:

        # get gene 
        inst_gene = inst_line[0]
        # add gene to rows 
        self.dat['nodes']['row'].append(inst_gene)

        # not going to do this here
        ############################
        # # add protein type to classification and initialize class to other
        # inst_prot_class = 'other'
        # for inst_gc in gc:
        #   if inst_gene in gc[inst_gc]:
        #     inst_prot_class = inst_gc
        # # add class to node_info
        # self.dat['node_info']['row']['cl'].append(inst_prot_class)

        # grab data, convert to float, and make numpy array 
        inst_data_row = inst_line[3:]
        inst_data_row = [float(tmp_dat) for tmp_dat in inst_data_row]

        inst_data_row = np.asarray(inst_data_row)

        # threshold data 
        inst_data_row[abs(inst_data_row) < thresh_data] = 0

        # initialize matrix 
        if i == 3:
          self.dat['mat'] = inst_data_row

        # add rows to matrix 
        if i > 3:
          self.dat['mat'] = np.vstack( ( self.dat['mat'], inst_data_row ) )


    print('\nthere are ' + str(len(self.dat['nodes']['row'])) + ' genes' )
    print('there are ' + str(len(self.dat['nodes']['col'])) + ' resources\n' )
    print('matrix shape')
    print(self.dat['mat'].shape)

  def load_l1000cds2(self, l1000cds2):
    import scipy
    import numpy as np
    
    # process gene set result 
    if 'upGenes' in l1000cds2['input']['data']:

      # add the names from all the results 
      all_results = l1000cds2['result']

      # grab col nodes - input sig and drugs 
      self.dat['nodes']['col'] = []

      for i in range(len(all_results)):
        inst_result = all_results[i]
        self.dat['nodes']['col'].append(inst_result['name']+'#'+str(i))

        self.dat['node_info']['col']['value'].append(inst_result['score'])

        for type_overlap in inst_result['overlap']:
          self.dat['nodes']['row'].extend( inst_result['overlap'][type_overlap] )


      self.dat['nodes']['row'] = sorted(list(set(self.dat['nodes']['row'])))

      # initialize the matrix 
      self.dat['mat'] = scipy.zeros([ len(self.dat['nodes']['row']), len(self.dat['nodes']['col']) ])

      # fill in the matrix with l10000 data 
      ########################################

      # fill in gene sigature as first column 
      for i in range(len(self.dat['nodes']['row'])):

        inst_gene = self.dat['nodes']['row'][i]

        # get gene index 
        inst_gene_index = self.dat['nodes']['row'].index(inst_gene)

        # if gene is in up add 1 otherwise add -1 
        if inst_gene in l1000cds2['input']['data']['upGenes']:
          self.dat['node_info']['row']['value'].append(1)
        else:
          self.dat['node_info']['row']['value'].append(-1)

      # save the name as a class
      for i in range(len(self.dat['nodes']['col'])):  
        self.dat['node_info']['col']['cl'].append(self.dat['nodes']['col'][i])

      # loop through drug results 
      for inst_result_index in range(len(all_results)):

        inst_result = all_results[inst_result_index]

        # if up/dn then it should be negative since the drug is dn 
        for inst_dn in inst_result['overlap']['up/dn']:

          # get gene index 
          inst_gene_index = self.dat['nodes']['row'].index(inst_dn)

          # save -1 to gene row and drug column 
          self.dat['mat'][ inst_gene_index, inst_result_index ] = -1 
         
        # if dn/up then it should be positive since the drug is up 
        for inst_up in inst_result['overlap']['dn/up']:

          # get gene index
          inst_gene_index = self.dat['nodes']['row'].index(inst_up)

          # save 1 to gene row and drug column 
          self.dat['mat'][ inst_gene_index, inst_result_index ] = 1

    # process a characteristic direction vector result
    else:
      all_results = l1000cds2['result']

      # get gene names 
      self.dat['nodes']['row'] = l1000cds2['input']['data']['up']['genes'] + l1000cds2['input']['data']['dn']['genes']

      # save gene expression values 
      tmp_exp_vect = l1000cds2['input']['data']['up']['vals'] + l1000cds2['input']['data']['dn']['vals']
      for i in range(len(self.dat['nodes']['row'])):
        self.dat['node_info']['row']['value'].append(tmp_exp_vect[i])

      # gather result names 
      for i in range(len(all_results)):

        inst_result = all_results[i]
        # add result to list 
        self.dat['nodes']['col'].append(inst_result['name']+'#'+str(i))
        self.dat['node_info']['col']['cl'].append(inst_result['name'])

        # reverse signature, score [1,2]
        if l1000cds2['input']['aggravate'] == False:
          self.dat['node_info']['col']['value'].append( inst_result['score']-1 )
        else:
          self.dat['node_info']['col']['value'].append( 1 - inst_result['score'] )

        # concat up and down lists 
        inst_vect = inst_result['overlap']['up'] + inst_result['overlap']['dn']
        inst_vect = np.transpose(np.asarray(inst_vect))

        inst_vect = inst_vect.reshape(-1,1)

        # initialize or add to matrix 
        if type(self.dat['mat']) is list:
          self.dat['mat'] = inst_vect
        else:
          self.dat['mat'] = np.hstack(( self.dat['mat'], inst_vect))

  def load_cst_kea_enr_to_net(self, enr, pval_cutoff):
    import scipy
    import numpy as np

    # enr - data structure 
      # cell line 
        # up_genes, dn_genes
          # name, pval, pval_bon, pval_bh, int_genes 

    print('loading cst enriched kinases ')

    # the columns are the cell lines 
    all_col = sorted(enr.keys())

    # the rows are the enriched terms 
    all_row = []

    # gather all genes with significantly enriched pval_bh 
    #######################################################
    updn = ['up','dn']
    # loop through cell lines 
    for inst_cl in enr:
      # loop through up/dn genes 
      for inst_updn in updn:

        # get inst_enr: the enrichment results from a cell line in either up/dn
        inst_enr = enr[inst_cl][inst_updn]

        # loop through enriched terms 
        for i in range(len(inst_enr)):

          # append name if pval is significant 
          if inst_enr[i]['pval_bh'] <= pval_cutoff:

            # append name to all terms 
            all_row.append(inst_enr[i]['name'])

    # get unique terms, sort them
    all_row = sorted(list(set(all_row)))

    # save row and column data to nodes 
    nodes = {}
    nodes['row'] = all_row
    nodes['col'] = all_col

    # gather data into matrix 
    #############################
    # initialize data_mat
    data_mat = {}
    data_mat['value']    = scipy.zeros([ len(all_row), len(all_col) ])
    data_mat['value_up'] = scipy.zeros([ len(all_row), len(all_col) ])
    data_mat['value_dn'] = scipy.zeros([ len(all_row), len(all_col) ])  

    # save additional informaiton in a dictionary 
    mat_info = {}

    # loop through the rows (genes)
    for i in range(len(all_row)):
      
      # get inst row: gene 
      inst_gene = all_row[i]

      # loop through the columns (cell lines)
      for j in range(len(all_col)):

        # get inst col: cell line 
        inst_cl = all_col[j]

        # initialize pval_nl negative log up/dn
        pval_nl = {}

        # ini list of substrates 
        substrates = []

        # get enrichment from up/dn genes
        for inst_updn in updn:

          # initialize pval_nl[inst_updn] = np.nan
          pval_nl[inst_updn] = np.nan

          # gather the current set of enrichment results
          # from the cell line 
          inst_enr = enr[inst_cl][inst_updn]

          # check if kinase is in list of enriched results 
          if any(d['name'] == inst_gene for d in inst_enr):

            # get the dict from the list
            inst_dict = self.find_dict_in_list( inst_enr, 'name', inst_gene)
            
            # only include significant pvalues
            if inst_dict['pval_bh'] <= 0.05:

              # retrieve the negative log pval_
              pval_nl[inst_updn] = -np.log2( inst_dict['pval_bh'] )

              # save ranks of substrates 
              substrates.extend( inst_dict['ranks'] )

            else:
              # set nan pval
              pval_nl[inst_updn] = np.nan

        # set value for data_mat 
        ###########################
        # now that the enrichment results have been gathered
        # for up/dn genes save the results 

        # there is both up and down enrichment 
        if np.isnan(pval_nl['up']) == False and np.isnan(pval_nl['dn']) == False:
          
          # set value of data_mat['merge'] as the mean of up/dn enrichment 
          data_mat['value'][i,j] = np.mean([ pval_nl['up'], -pval_nl['dn'] ])

          # set values of up/dn
          data_mat['value_up'][i,j] =  pval_nl['up']
          data_mat['value_dn'][i,j] = -pval_nl['dn']

        # there is only up enrichment 
        elif np.isnan(pval_nl['up']) == False:
          # set value of data_mat as up enrichment 
          data_mat['value'][i,j] = pval_nl['up'] 
          data_mat['value_up'][i,j] = pval_nl['up']

        # there is only dn enrichment
        elif np.isnan(pval_nl['dn']) == False:
          # set value of data_mat as the mean of up/dn enrichment 
          data_mat['value'][i,j] = -pval_nl['dn']
          data_mat['value_dn'][i,j] = -pval_nl['dn']

        # save substrates to mat_info
        mat_info[(i,j)] = substrates

    # save nodes and data_mat to self.dat
    self.dat['nodes'] = nodes
    self.dat['mat'] = data_mat['value']

    # add up and dn values into self.dat
    self.dat['mat_up'] = data_mat['value_up']
    self.dat['mat_dn'] = data_mat['value_dn']

    # add mat_info with substrate information 
    self.dat['mat_info'] = mat_info

  def load_ccle_to_net(self, prot_type):
    import scipy 
    import numpy as np

    # load ccle data 
    ccle = self.load_json_to_dict('CCLE/nsclc_allzc.json')
    ccle['data_z'] = np.asarray(ccle['data_z'], dtype = float)

    # load protein type lists 
    gs_list = self.load_json_to_dict('gene_classes_harmonogram.json')

    # generate node lists 
    # find the protein-types that are in ccle 
    self.dat['nodes']['row'] = sorted(list(set(gs_list[prot_type]).intersection(ccle['gene'])))
    self.dat['nodes']['col'] = ccle['cell_lines']


    # initialize mat
    self.dat['mat'] = scipy.zeros([ len(self.dat['nodes']['row']), len(self.dat['nodes']['col']) ])

    # loop through rows and cols
    for i in range(len(self.dat['nodes']['row'])):
      for j in range(len(self.dat['nodes']['col'])):

        # get inst_row and inst_col
        inst_row = self.dat['nodes']['row'][i]
        inst_col = self.dat['nodes']['col'][j]

        # find gene and cl index in zscored data 
        index_x = ccle['gene'].index(inst_row)
        index_y = ccle['cell_lines'].index(inst_col)

        # map primary data to mat 
        self.dat['mat'][i,j] = ccle['data_z'][index_x, index_y]

  def load_g2e_to_net(self, g2e):
    import numpy as np

    # get all signatures 
    sigs = g2e['gene_signatures']

    # get all genes from signatures 
    all_genes = []
    all_sigs = []
    for inst_sig in sigs:

      # get gene data 
      gene_data = inst_sig['genes']

      # gather sig names 
      all_sigs.append(inst_sig['col_title']) 

      # gather genes 
      for inst_gene_data in gene_data:

        # add genes - the gene name is the first element of the list 
        all_genes.append( inst_gene_data[0] )

    # get unique sorted list of genes 
    all_genes = sorted(list(set(all_genes)))
    print( 'found ' + str(len(all_genes)) + ' genes' )
    print( 'found ' + str(len(all_sigs)) + ' siguatures\n'  )

    # save genes and sigs to nodes 
    self.dat['nodes']['row'] = all_genes
    self.dat['nodes']['col'] = all_sigs

    # initialize numpy matrix of nans
    self.dat['mat'] = np.empty((len(all_genes),len(all_sigs)))
    self.dat['mat'][:] = np.nan

    # loop through all signatures and genes 
    # and place information into self.dat
    for inst_sig in sigs:

      # get sig name 
      inst_sig_name = inst_sig['col_title']

      # get gene data
      gene_data = inst_sig['genes']

      # loop through genes 
      for inst_gene_data in gene_data:

        # add gene data to signature matrix 
        inst_gene = inst_gene_data[0]
        inst_value = inst_gene_data[1]

        # find index of gene and sig in matrix 
        row_index = all_genes.index(inst_gene)
        col_index  = all_sigs.index(inst_sig_name)

        # save inst_value to matrix 
        self.dat['mat'][row_index, col_index] = inst_value

  def load_data_file_to_net(self, filename):
    # load json from file to new dictionary 
    inst_dat = self.load_json_to_dict(filename)
    # convert dat['mat'] to numpy array and add to network 
    self.load_data_to_net(inst_dat)

  def load_data_to_net(self, inst_net):
    ''' load data into nodes and mat, also convert mat to numpy array''' 
    self.dat['nodes'] = inst_net['nodes']
    self.dat['mat'] = inst_net['mat']
    # convert to numpy array 
    self.mat_to_numpy_arr()

  def export_net_json(self, net_type, indent='no-indent'):
    ''' export json string of dat '''
    import json 
    from copy import deepcopy

    if net_type == 'dat':
      exp_dict = deepcopy(self.dat)

      # convert numpy array to list 
      if type(exp_dict['mat']) is not list:
        exp_dict['mat'] = exp_dict['mat'].tolist()

    elif net_type == 'viz':
      exp_dict = self.viz

    # make json 
    if indent == 'indent':
      exp_json = json.dumps(exp_dict, indent=2)
    else:
      exp_json = json.dumps(exp_dict)

    return exp_json

  def write_json_to_file(self, net_type, filename, indent='no-indent'):
    import json 

    # get dat or viz representation as json string 
    if net_type == 'dat':
      exp_json = self.export_net_json('dat', indent)
    elif net_type == 'viz':
      exp_json = self.export_net_json('viz', indent)

    # save to file 
    fw = open(filename, 'w')
    fw.write( exp_json ) 
    fw.close()

  def set_node_names(self, row_name, col_name):
    '''give names to the rows and columns'''
    self.dat['node_names'] = {}
    self.dat['node_names']['row'] = row_name
    self.dat['node_names']['col'] = col_name

  def mat_to_numpy_arr(self):
    ''' convert list to numpy array - numpy arrays can not be saved as json '''
    import numpy as np
    self.dat['mat'] = np.asarray( self.dat['mat'] )

  def swap_nan_for_zero(self):
    import numpy as np
    self.dat['mat'][ np.isnan( self.dat['mat'] ) ] = 0

  def filter_row_thresh( self, row_filt_int, filter_type='value' ):
    ''' 
    Remove rows from matrix that do not meet some threshold

    value: The default filtering is value, in that at least one value in the row 
    has to be higher than some threshold. 

    num: Rows can be filtered by the number of non-zero values it has. 

    sum: Rows can be filtered by the sum of the values 

    '''
    import scipy
    import numpy as np

    # max vlue in matrix 
    mat = self.dat['mat']
    max_mat = abs(max(mat.min(), mat.max(), key=abs))
    # maximum number of measurements 
    max_num = len(self.dat['nodes']['col'])

    mat_abs = abs(mat)
    sum_row = np.sum(mat_abs, axis=1)
    max_sum = max(sum_row)

    # transfer the nodes 
    nodes = {}
    nodes['row'] = []
    nodes['col'] = self.dat['nodes']['col']

    # transfer the 'info' part of node_info if necessary 
    node_info = {}
    node_info['row'] = []
    node_info['col'] = self.dat['node_info']['col']['info']

    # filter rows  
    #################################
    for i in range(len(self.dat['nodes']['row'])):

      # get row name 
      inst_nodes_row = self.dat['nodes']['row'][i]

      # get node info - disregard ini, clust, and rank orders
      if len(self.dat['node_info']['row']['info']) > 0:
        inst_node_info = self.dat['node_info']['row']['info'][i]

      # get absolute value of row data 
      row_vect = np.absolute(self.dat['mat'][i,:])

      # value: is there at least one value over cutoff 
      ##################################################
      if filter_type == 'value':

        # calc cutoff 
        cutoff = row_filt_int * max_mat

        # count the number of values above some thresh 
        found_tuple = np.where(row_vect >= cutoff)
        if len(found_tuple[0])>=1:
          # add name 
          nodes['row'].append(inst_nodes_row)
          # add info if necessary 
          if len(self.dat['node_info']['row']['info']) > 0:
            node_info['row'].append(inst_node_info)

      elif filter_type == 'num':

        num_nonzero = np.count_nonzero(row_vect)
        # use integer number of non-zero measurements
        cutoff = row_filt_int * 10

        # print('num_nonzero '+str(num_nonzero)+' cutoff: '+str(cutoff))
        # print('\n')

        if num_nonzero>= cutoff:
          # add name 
          nodes['row'].append(inst_nodes_row)
          # add info if necessary 
          if len(self.dat['node_info']['row']['info']) > 0:
            node_info['row'].append(inst_node_info)

      elif filter_type == 'sum':

        inst_row_sum = sum(abs(row_vect))

        if inst_row_sum > row_filt_int*max_sum:
          # add name 
          nodes['row'].append(inst_nodes_row)
          # add info if necessary 
          if len(self.dat['node_info']['row']['info']) > 0:
            node_info['row'].append(inst_node_info)

    # cherrypick data from self.dat['mat'] 
    ##################################
    # filtered matrix 
    filt_mat = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_up' in self.dat:  
      filt_mat_up = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
      filt_mat_dn = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_info' in self.dat:
      # initialize filtered mat_info dictionary with tuple keys 
      filt_mat_info = {}

    # loop through the rows
    for i in range(len(nodes['row'])):
      inst_row = nodes['row'][i]

      # loop through the cols
      for j in range(len(nodes['col'])):

        inst_col = nodes['col'][j]

        # get row and col index
        pick_row = self.dat['nodes']['row'].index(inst_row)
        pick_col = self.dat['nodes']['col'].index(inst_col)

        # cherrypick 
        ###############
        filt_mat[i,j] = self.dat['mat'][pick_row, pick_col]
        if 'mat_up' in self.dat:  
          filt_mat_up[i,j] = self.dat['mat_up'][pick_row, pick_col]
          filt_mat_dn[i,j] = self.dat['mat_dn'][pick_row, pick_col]
        if 'mat_info' in self.dat:
          filt_mat_info[str((i,j))] = self.dat['mat_info'][str((pick_row,pick_col))]

    # save nodes array - list of node names 
    self.dat['nodes'] = nodes

    # save node_info array - list of node infos 
    self.dat['node_info']['row']['info'] = node_info['row']
    self.dat['node_info']['col']['info'] = node_info['col']

    # overwrite with new filtered data 
    self.dat['mat'] = filt_mat
    # overwrite with up/dn data if necessary 
    if 'mat_up' in self.dat:  
      self.dat['mat_up'] = filt_mat_up
      self.dat['mat_dn'] = filt_mat_dn
    # overwrite mat_info if necessary 
    if 'mat_info' in self.dat:
      self.dat['mat_info'] = filt_mat_info

    print( 'final mat shape' + str(self.dat['mat'].shape ) + '\n')

  def filter_col_thresh( self, cutoff, min_num_meet ):
    ''' 
    remove rows and columns from matrix that do not have at least 
    min_num_meet instances of a value with an absolute value above cutoff 
    '''
    import scipy
    import numpy as np

    # transfer the nodes 
    nodes = {}
    nodes['row'] = self.dat['nodes']['row']
    nodes['col'] = []

    # transfer the 'info' part of node_info if necessary 
    node_info = {}
    node_info['row'] = self.dat['node_info']['row']['info']
    node_info['col'] = []

    # add cols with non-zero values 
    #################################
    for i in range(len(self.dat['nodes']['col'])):

      # get col name
      inst_nodes_col = self.dat['nodes']['col'][i]

      # get node info - disregard ini, clust, and rank orders
      if len(self.dat['node_info']['col']['info']) > 0:
        inst_node_info = self.dat['node_info']['col']['info'][i]

      # get col vect 
      col_vect = np.absolute(self.dat['mat'][:,i])

      # check if there are nonzero values
      found_tuple = np.where(col_vect >= cutoff)
      if len(found_tuple[0])>=min_num_meet:

        # add name
        nodes['col'].append(inst_nodes_col)

        # add info if necessary 
        if len(self.dat['node_info']['col']['info']) > 0:
          node_info['col'].append(inst_node_info)

    # cherrypick data from self.dat['mat'] 
    ##################################
    # filtered matrix 
    filt_mat = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_up' in self.dat:  
      filt_mat_up = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
      filt_mat_dn = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_info' in self.dat:
      # initialize filtered mat_info dictionary with tuple keys 
      filt_mat_info = {}

    # loop through the rows
    for i in range(len(nodes['row'])):
      inst_row = nodes['row'][i]
      # loop through the cols
      for j in range(len(nodes['col'])):
        inst_col = nodes['col'][j]

        # get row and col index
        pick_row = self.dat['nodes']['row'].index(inst_row)
        pick_col = self.dat['nodes']['col'].index(inst_col)

        # cherrypick 
        ###############
        filt_mat[i,j] = self.dat['mat'][pick_row, pick_col]
        if 'mat_up' in self.dat:  
          filt_mat_up[i,j] = self.dat['mat_up'][pick_row, pick_col]
          filt_mat_dn[i,j] = self.dat['mat_dn'][pick_row, pick_col]
        if 'mat_info' in self.dat:
          filt_mat_info[str((i,j))] = self.dat['mat_info'][str((pick_row,pick_col))]

    # save nodes array - list of node names 
    self.dat['nodes'] = nodes

    # save node_info array - list of node infos 
    self.dat['node_info']['row']['info'] = node_info['row']
    self.dat['node_info']['col']['info'] = node_info['col']

    # overwrite with new filtered data 
    self.dat['mat'] = filt_mat
    # overwrite with up/dn data if necessary 
    if 'mat_up' in self.dat:  
      self.dat['mat_up'] = filt_mat_up
      self.dat['mat_dn'] = filt_mat_dn
    # overwrite mat_info if necessary 
    if 'mat_info' in self.dat:
      self.dat['mat_info'] = filt_mat_info

    print( 'final mat shape' + str(self.dat['mat'].shape ) + '\n')

  def filter_network_thresh( self, cutoff, min_num_meet ):
    ''' 
    remove rows and columns from matrix that do not have at least 
    min_num_meet instances of a value with an absolute value above cutoff 
    '''
    import scipy
    import numpy as np

    # transfer the nodes 
    nodes = {}
    nodes['row'] = []
    nodes['col'] = []

    # transfer the 'info' part of node_info if necessary 
    node_info = {}
    node_info['row'] = []
    node_info['col'] = []

    # add rows with non-zero values 
    #################################
    for i in range(len(self.dat['nodes']['row'])):

      # get row name 
      inst_nodes_row = self.dat['nodes']['row'][i]

      # get node info - disregard ini, clust, and rank orders
      if len(self.dat['node_info']['row']['info']) > 0:
        inst_node_info = self.dat['node_info']['row']['info'][i]

      # get row vect 
      row_vect = np.absolute(self.dat['mat'][i,:])

      # check if there are nonzero values 
      found_tuple = np.where(row_vect >= cutoff)
      if len(found_tuple[0])>=min_num_meet:

        # add name 
        nodes['row'].append(inst_nodes_row)

        # add info if necessary 
        if len(self.dat['node_info']['row']['info']) > 0:
          node_info['row'].append(inst_node_info)

    # add cols with non-zero values 
    #################################
    for i in range(len(self.dat['nodes']['col'])):

      # get col name
      inst_nodes_col = self.dat['nodes']['col'][i]

      # get node info - disregard ini, clust, and rank orders
      if len(self.dat['node_info']['col']['info']) > 0:
        inst_node_info = self.dat['node_info']['col']['info'][i]

      # get col vect 
      col_vect = np.absolute(self.dat['mat'][:,i])

      # check if there are nonzero values
      found_tuple = np.where(col_vect >= cutoff)
      if len(found_tuple[0])>=min_num_meet:

        # add name
        nodes['col'].append(inst_nodes_col)

        # add info if necessary 
        if len(self.dat['node_info']['col']['info']) > 0:
          node_info['col'].append(inst_node_info)

    # cherrypick data from self.dat['mat'] 
    ##################################
    # filtered matrix 
    filt_mat = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_up' in self.dat:  
      filt_mat_up = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
      filt_mat_dn = scipy.zeros([ len(nodes['row']), len(nodes['col']) ])
    if 'mat_info' in self.dat:
      # initialize filtered mat_info dictionary with tuple keys 
      filt_mat_info = {}

    # loop through the rows
    for i in range(len(nodes['row'])):
      inst_row = nodes['row'][i]
      # loop through the cols
      for j in range(len(nodes['col'])):
        inst_col = nodes['col'][j]

        # get row and col index
        pick_row = self.dat['nodes']['row'].index(inst_row)
        pick_col = self.dat['nodes']['col'].index(inst_col)

        # cherrypick 
        ###############
        filt_mat[i,j] = self.dat['mat'][pick_row, pick_col]
        if 'mat_up' in self.dat:  
          filt_mat_up[i,j] = self.dat['mat_up'][pick_row, pick_col]
          filt_mat_dn[i,j] = self.dat['mat_dn'][pick_row, pick_col]
        if 'mat_info' in self.dat:
          filt_mat_info[str((i,j))] = self.dat['mat_info'][str((pick_row,pick_col))]

    # save nodes array - list of node names 
    self.dat['nodes'] = nodes

    # save node_info array - list of node infos 
    self.dat['node_info']['row']['info'] = node_info['row']
    self.dat['node_info']['col']['info'] = node_info['col']

    # overwrite with new filtered data 
    self.dat['mat'] = filt_mat
    # overwrite with up/dn data if necessary 
    if 'mat_up' in self.dat:  
      self.dat['mat_up'] = filt_mat_up
      self.dat['mat_dn'] = filt_mat_dn
    # overwrite mat_info if necessary 
    if 'mat_info' in self.dat:
      self.dat['mat_info'] = filt_mat_info

    print( 'final mat shape' + str(self.dat['mat'].shape ) + '\n')

  def keep_max_num_links(self, keep_num_links):

    print('\trun keep_max_num_links')
    max_mat_value = abs(self.dat['mat']).max()

    # check the total number of links 
    inst_thresh = 0
    inst_pct_max = 0
    inst_num_links = (abs(self.dat['mat'])>inst_thresh).sum()
    print('initially there are '+str(inst_num_links)+' links ')

    print('there are initially '+str(inst_num_links)+'\n')

    thresh_fraction = 100

    while (inst_num_links > keep_num_links):

      # increase the threshold as a pct of max value in mat 
      inst_pct_max = inst_pct_max + 1 

      # increase threshold 
      inst_thresh = max_mat_value*(float(inst_pct_max)/thresh_fraction)

      # check the number of links above the curr threshold 
      inst_num_links = (abs(self.dat['mat'])>inst_thresh).sum()

      print('there are '+str(inst_num_links)+ ' links at threshold '+str(inst_pct_max)+'pct and value of ' +str(inst_thresh)+'\n')

    # if there are no links then increas thresh back up 
    if inst_num_links == 0:
      inst_pct_max = inst_pct_max - 1 
      inst_thresh = max_mat_value*(float(inst_pct_max)/thresh_fraction)

    print('final number of links '+str(inst_num_links))

    # replace values that are less than thresh with zero 
    self.dat['mat'][ abs(self.dat['mat']) < inst_thresh] = 0

    # return number of links 
    return (abs(self.dat['mat'])>inst_thresh).sum()

  def cluster_row_and_col(self, dist_type, cutoff=0, min_num_comp=1, dendro=True, run_clustering=True, run_rank=True):
    ''' 
    cluster net.dat and make visualization json, net.viz. 
    optionally leave out dendrogram colorbar groups with dendro argument 
    '''
    import scipy
    import numpy as np 
    from scipy.spatial.distance import pdist
    from copy import deepcopy

    # do not make dendrogram is you are not running clusttering 
    if run_clustering == False:
      dendro = False


    # make distance matrices 
    ##########################

    # get number of rows and columns from self.dat 
    num_row = len(self.dat['nodes']['row'])
    num_col = len(self.dat['nodes']['col'])

    # initialize distance matrices 
    row_dm = scipy.zeros([num_row,num_row])
    col_dm = scipy.zeros([num_col,num_col])

    # make copy of matrix 
    tmp_mat = deepcopy(self.dat['mat'])

    # calculate distance matrix 
    row_dm = pdist( tmp_mat, metric='cosine' )
    col_dm = pdist( tmp_mat.transpose(), metric='cosine' )

    # prevent negative values 
    # row 
    row_dm[row_dm < 0] = float(0)
    # col
    col_dm[col_dm < 0] = float(0)

    # initialize clust order 
    clust_order = self.ini_clust_order()

    # initial ordering
    ###################
    clust_order['row']['ini'] = range(num_row, -1, -1)
    clust_order['col']['ini'] = range(num_col, -1, -1)

    # cluster 
    ##############
    if run_clustering == True:
      # cluster rows 
      cluster_method = 'average'
      clust_order['row']['clust'], clust_order['row']['group'] = self.clust_and_group_nodes(row_dm, cluster_method)
      clust_order['col']['clust'], clust_order['col']['group'] = self.clust_and_group_nodes(col_dm, cluster_method)

    if run_rank == True:
      # rank 
      ############
      clust_order['row']['rank'] = self.sort_rank_nodes('row')
      clust_order['col']['rank'] = self.sort_rank_nodes('col')

    # save clustering orders to node_info 
    if run_clustering == True:
      print('\n\ntransferring clustering orders\n\n')
      self.dat['node_info']['row']['clust'] = clust_order['row']['clust']
      self.dat['node_info']['col']['clust'] = clust_order['col']['clust']
    else:
      print('\n\nnot transferring clustering orders\n\n')
      self.dat['node_info']['row']['clust'] = clust_order['row']['ini']
      self.dat['node_info']['col']['clust'] = clust_order['col']['ini']

    if run_rank == True:
      self.dat['node_info']['row']['rank']  = clust_order['row']['rank']
      self.dat['node_info']['col']['rank']  = clust_order['col']['rank']
    else:
      self.dat['node_info']['row']['rank']  = clust_order['row']['ini']
      self.dat['node_info']['col']['rank']  = clust_order['col']['ini']

    # transfer ordereings
    # row
    self.dat['node_info']['row']['ini']   = clust_order['row']['ini']
    self.dat['node_info']['row']['group'] = clust_order['row']['group']
    # col 
    self.dat['node_info']['col']['ini']   = clust_order['col']['ini']
    self.dat['node_info']['col']['group'] = clust_order['col']['group']


    # make the viz json - can optionally leave out dendrogram
    self.viz_json(dendro)

  def clust_and_group_nodes( self, dm, cluster_method ):
    import scipy.cluster.hierarchy as hier

    # calculate linkage 
    Y = hier.linkage( dm, method=cluster_method )
    Z = hier.dendrogram( Y, no_plot=True )
    # get ordering
    inst_clust_order = Z['leaves']

    all_dist = self.group_cutoffs()

    # generate distance cutoffs 
    inst_groups = {}
    for inst_dist in all_dist:
      inst_key = str(inst_dist).replace('.','')
      inst_groups[inst_key] = hier.fcluster(Y, inst_dist*dm.max(), 'distance') 
      inst_groups[inst_key] = inst_groups[inst_key].tolist()

    return inst_clust_order, inst_groups

  def sort_rank_node_values( self, rowcol ):
    import numpy as np
    from operator import itemgetter
    from copy import deepcopy

    # make a copy of nodes and node_info
    inst_nodes = deepcopy(self.dat['nodes'][rowcol])
    inst_vals  = deepcopy(self.dat['node_info'][rowcol]['value'])

    tmp_arr = []
    for i in range(len(inst_nodes)):
      inst_dict = {}
      # get name of the node 
      inst_dict['name'] = inst_nodes[i]
      # get value 
      inst_dict['value'] = inst_vals[i]
      tmp_arr.append(inst_dict)

    # sort dictionary by value 
    tmp_arr = sorted( tmp_arr, key=itemgetter('value') )

    # get list of sorted nodes 
    tmp_sort_nodes = []
    for inst_dict in tmp_arr:
      tmp_sort_nodes.append( inst_dict['name'] )

    # get the sorted index 
    sort_index = []
    for inst_node in inst_nodes:
      sort_index.append( tmp_sort_nodes.index(inst_node) )

    return sort_index

  def sort_rank_nodes( self, rowcol ):
    import numpy as np
    from operator import itemgetter
    from copy import deepcopy

    # make a copy of node information 
    inst_nodes = deepcopy(self.dat['nodes'][rowcol])
    inst_mat   = deepcopy(self.dat['mat'])

    sum_term = []
    for i in range(len(inst_nodes)):
      inst_dict = {}
      # get name of the node 
      inst_dict['name'] = inst_nodes[i]
      # sum values of the node
      if rowcol == 'row':
        inst_dict['total'] = np.sum(inst_mat[i,:])
      else:
        inst_dict['total'] = np.sum(inst_mat[:,i])
      # add this to the list of dicts 
      sum_term.append(inst_dict)

    # sort dictionary by number of terms 
    sum_term = sorted( sum_term, key=itemgetter('total'), reverse=False )
    # get list of sorted nodes 
    tmp_sort_nodes = []
    for inst_dict in sum_term:
      tmp_sort_nodes.append(inst_dict['name'])

    # get the sorted index
    sort_index = []
    for inst_node in inst_nodes:
      sort_index.append( tmp_sort_nodes.index(inst_node) )

    return sort_index

  def calc_thresh_col_dist( self, vect_row, vect_col, cutoff, min_num_meet):
    import scipy.spatial
    import numpy as np

    # apply cutoff 
    vect_row, vect_col = self.threshold_vect_comparison(vect_row, vect_col, cutoff)

    # check min_num_meet 
    if len(vect_row) >= min_num_meet:
      inst_dist = scipy.spatial.distance.cosine(vect_row, vect_col)
    else:
      # later the nans will be replaced with the maximum distance 
      inst_dist = np.nan

    return inst_dist

  def viz_json(self, dendro=True):
    ''' make the dictionary for the clustergram.js visualization '''

    print('in viz_json')
    # get dendrogram cutoff distances 
    all_dist = self.group_cutoffs()

    print('viz_json: set up nodes')
    # make nodes for viz
    #####################
    # make rows and cols 
    for inst_rc in self.dat['nodes']:

      for i in range(len( self.dat['nodes'][inst_rc] )):
        inst_dict = {}
        inst_dict['name']  = self.dat['nodes'][inst_rc][i]
        inst_dict['ini']   = self.dat['node_info'][inst_rc]['ini'][i]
        #!! clean this up so I do not have to get the index here 
        inst_dict['clust'] = self.dat['node_info'][inst_rc]['clust'].index(i)
        inst_dict['rank']  = self.dat['node_info'][inst_rc]['rank'][i]

        # add node class 'cl' - this could potentially be a list of several classes 
        # if 'cl' in self.dat['node_info'][inst_rc]:
        if len(self.dat['node_info'][inst_rc]['cl']) > 0:
          inst_dict['cl'] = self.dat['node_info'][inst_rc]['cl'][i]
        if len(self.dat['node_info'][inst_rc]['value']) > 0:
          inst_dict['value'] = self.dat['node_info'][inst_rc]['value'][i]

        # add node information 
        # if 'info' in self.dat['node_info'][inst_rc]:
        if len(self.dat['node_info'][inst_rc]['info']) > 0:
          inst_dict['info'] = self.dat['node_info'][inst_rc]['info'][i]

        # group info 
        if dendro==True:
          inst_dict['group'] = []
          for tmp_dist in all_dist:
            # read group info in correct order 
            tmp_dist = str(tmp_dist).replace('.','')
            inst_dict['group'].append( float( self.dat['node_info'][inst_rc]['group'][tmp_dist][i] ) )

        # append dictionary to list of nodes
        self.viz[inst_rc+'_nodes'].append(inst_dict)

    print('viz_json: set up links')
    # links 
    ########
    for i in range(len( self.dat['nodes']['row'] )):
      for j in range(len( self.dat['nodes']['col'] )):
        if abs( self.dat['mat'][i,j] ) > 0:
          inst_dict = {}
          inst_dict['source'] = i
          inst_dict['target'] = j 
          inst_dict['value'] = self.dat['mat'][i,j]

          # add up/dn values if necessary 
          if 'mat_up' in self.dat:
            inst_dict['value_up'] = self.dat['mat_up'][i,j]
          if 'mat_up' in self.dat:
            inst_dict['value_dn'] = self.dat['mat_dn'][i,j]

          # add information if necessary - use dictionary with tuple key
          # each element of the matrix needs to have information 
          if 'mat_info' in self.dat:

            # use tuple string 
            inst_dict['info'] = self.dat['mat_info'][str((i,j))]

          # add highlight if necessary - use dictionary with tuple key 
          if 'mat_hl' in self.dat:
            inst_dict['highlight'] = self.dat['mat_hl'][i,j]

          # append link 
          self.viz['links'].append( inst_dict )

  def df_to_dat(self, df):
    import numpy as np 
    import pandas as pd 

    self.dat['mat'] = df.values
    self.dat['nodes']['row'] = df.index.tolist()
    self.dat['nodes']['col'] = df.columns.tolist()

  def make_mult_views(self, dist_type='cos',filter_row=['value'], filter_col=False, run_clustering=True, dendro=True):
    ''' 
    This will calculate multiple views of a clustergram by filtering the 
    data and clustering after each fitlering. By default row filtering will 
    be turned on and column filteirng will not. The filtering steps are defined
    as a percentage of the maximum value found in the network. 
    '''
    from clustergrammer import Network
    from copy import deepcopy 

    # filter between 0% and 90% of some to be determined value 
    all_filt = range(10)
    all_filt = [i/float(10) for i in all_filt]

    # cluster default view 
    self.cluster_row_and_col('cos', run_clustering=run_clustering, dendro=dendro)

    self.viz['views'] = []

    all_views = []

    # Perform row filterings 
    ###########################
    if len(filter_row) > 0:

      # perform multiple types of row filtering 
      ###########################################
      for inst_type in filter_row:
        
        for row_filt_int in all_filt:

          # initialize new net 
          net = deepcopy(Network())
          net.dat = deepcopy(self.dat)
          # filter rows 
          net.filter_row_thresh(row_filt_int, filter_type=inst_type)

          # filter columns since some columns might be all zero 
          net.filter_col_thresh(0.001,1)

          # try to filter - will not work if there is one row
          try:

            # cluster 
            net.cluster_row_and_col('cos')

            inst_name = 'filter_row'+'_'+inst_type

            # add view 
            inst_view = {}
            inst_view[inst_name] = row_filt_int
            inst_view['dist'] = 'cos'
            inst_view['nodes'] = {}
            inst_view['nodes']['row_nodes'] = net.viz['row_nodes']
            inst_view['nodes']['col_nodes'] = net.viz['col_nodes']

            all_views.append(inst_view)

          except:
            print('did not cluster filtered view')

    # Default col Filtering 
    ###########################
    inst_meet = 1
    if filter_col == True:
      # col filtering 
      #####################
      for col_filt in all_filt:
        print(col_filt)
        # initialize new net 
        net = deepcopy(Network())
        net.dat = deepcopy(self.dat)
        filt_value = col_filt * max_mat
        # filter cols 
        net.filter_col_thresh(filt_value, inst_meet)

        # try to filter - will not work if there is one col
        try:

          # cluster 
          net.cluster_row_and_col('cos')

          # add view 
          inst_view = {}
          inst_view['filter_col'] = col_filt
          inst_view['dist'] = 'cos'
          inst_view['nodes'] = {}
          inst_view['nodes']['row_nodes'] = net.viz['row_nodes']
          inst_view['nodes']['col_nodes'] = net.viz['col_nodes']

          all_views.append(inst_view)

        except:
          print('did not cluster filtered view')    


    # add views to viz
    self.viz['views'] = all_views


  @staticmethod
  def load_gmt(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    gmt = {}

    # loop through the lines of the gmt 
    for i in range(len(lines)):

      # get the inst line, strip off the new line character 
      inst_line = lines[i].rstrip()

      inst_term = inst_line.split('\t')[0]

      # get the elements 
      inst_elems = inst_line.split('\t')[2:]

      # save the drug-kinase sets 
      gmt[inst_term] = inst_elems

    return gmt

  @staticmethod
  def load_json_to_dict(filename):
    ''' load json to python dict and return dict '''
    import json

    f = open(filename, 'r')
    inst_dict = json.load(f)
    f.close()
    return inst_dict 

  @staticmethod
  def save_dict_to_json(inst_dict, filename, indent='no-indent'):
    import json

    # save as a json 
    fw = open(filename, 'w')
    if indent == 'indent':
      fw.write( json.dumps(inst_dict, indent=2) )
    else:
      fw.write( json.dumps(inst_dict) )
    fw.close()

  @staticmethod
  def ini_clust_order():
    rowcol = ['row','col']
    orderings = ['clust','rank','group','ini']
    clust_order = {}
    for inst_node in rowcol:
      clust_order[inst_node] = {}

      for inst_order in orderings:
        clust_order[inst_node][inst_order] = []

    return clust_order

  @staticmethod
  def threshold_vect_comparison(x, y, cutoff):
    import numpy as np 

    # x vector 
    ############
    # take absolute value of x
    x_abs = np.absolute(x)
    # this returns a tuple 
    found_tuple = np.where(x_abs >= cutoff)
    # get index array 
    found_index_x = found_tuple[0]

    # y vector 
    ############
    # take absolute value of y
    y_abs = np.absolute(y)
    # this returns a tuple 
    found_tuple = np.where(y_abs >= cutoff)
    # get index array 
    found_index_y = found_tuple[0]

    # get common intersection 
    found_common = np.intersect1d(found_index_x, found_index_y)

    # apply cutoff 
    thresh_x = x[found_common]
    thresh_y = y[found_common]

    # return the threshold data 
    return thresh_x, thresh_y

  @staticmethod
  def group_cutoffs():
    # generate distance cutoffs
    all_dist = []
    for i in range(11):
      all_dist.append(float(i)/10)

    return all_dist

  @staticmethod
  def find_dict_in_list(list_dict, search_value, search_string):
    ''' find a dict in a list of dicts by searching for a value '''
    # get all the possible values of search_value
    all_values = [d[search_value] for d in list_dict]

    # check if the search value is in the keys 
    if search_string in all_values:
      # find the dict 
      found_dict = (item for item in list_dict if item[search_value] == search_string).next()
    else:
      found_dict = {}

    # return the found dictionary
    return found_dict

  