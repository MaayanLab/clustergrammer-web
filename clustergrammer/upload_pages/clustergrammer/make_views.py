def N_rows(net, df, all_views, dist_type='cosine', rank_type='sum'):
  from copy import deepcopy
  from __init__ import Network
  import calc_clust, run_filter

  keep_top = ['all', 500, 400, 300, 200, 100, 80, 60, 40, 20, 10]

  df_abs = deepcopy(df['mat'])
  df_abs = df_abs.transpose()

  if rank_type == 'sum':
    tmp_sum = df_abs.sum(axis=0)
  elif rank_type == 'var':
    tmp_sum = df_abs.var(axis=0)

  tmp_sum = tmp_sum.abs()
  tmp_sum.sort_values(inplace=True, ascending=False)
  rows_sorted = tmp_sum.index.values.tolist()

  for inst_keep in keep_top:

    tmp_df = deepcopy(df)

    if inst_keep < len(rows_sorted) or inst_keep == 'all':

      tmp_net = deepcopy(Network())

      if inst_keep != 'all':

        keep_rows = rows_sorted[0:inst_keep]
        tmp_df['mat'] = tmp_df['mat'].ix[keep_rows]

        if 'mat_up' in tmp_df:
          tmp_df['mat_up'] = tmp_df['mat_up'].ix[keep_rows]
          tmp_df['mat_dn'] = tmp_df['mat_dn'].ix[keep_rows]

        tmp_df = run_filter.df_filter_col(tmp_df, 0.001)
        tmp_net.df_to_dat(tmp_df)

      else:
        tmp_net.df_to_dat(tmp_df)

      try:
        try:
          calc_clust.cluster_row_and_col(tmp_net, dist_type, run_clustering=True)
        except:
          calc_clust.cluster_row_and_col(tmp_net, dist_type, run_clustering=False)

        # add view
        inst_view = {}
        inst_view['N_row_' + rank_type] = inst_keep
        inst_view['dist'] = 'cos'
        inst_view['nodes'] = {}
        inst_view['nodes']['row_nodes'] = tmp_net.viz['row_nodes']
        inst_view['nodes']['col_nodes'] = tmp_net.viz['col_nodes']
        all_views.append(inst_view)

      except:
        # print('\t*** did not cluster N filtered view')
        pass

  return all_views

def pct_rows(net, df, all_views, dist_type, rank_type):

  from __init__ import Network
  from copy import deepcopy
  import numpy as np
  import calc_clust, run_filter

  copy_net = deepcopy(net)

  if len(net.dat['node_info']['col']['cat']) > 0:
    cat_key_col = {}
    for i in range(len(net.dat['nodes']['col'])):
      cat_key_col[net.dat['nodes']['col'][i]] = \
          net.dat['node_info']['col']['cat'][i]

  all_filt = range(10)
  all_filt = [i / float(10) for i in all_filt]

  mat = deepcopy(df['mat'])
  sum_row = np.sum(mat, axis=1)
  max_sum = max(sum_row)

  for inst_filt in all_filt:

    cutoff = inst_filt * max_sum
    copy_net = deepcopy(net)
    inst_df = deepcopy(df)
    inst_df = run_filter.df_filter_row(inst_df, cutoff, take_abs=False)

    tmp_net = deepcopy(Network())
    tmp_net.df_to_dat(inst_df)

    try:
      try:
        calc_clust.cluster_row_and_col(tmp_net, dist_type=dist_type, 
                                       run_clustering=True)

      except:
        calc_clust.cluster_row_and_col(tmp_net, dist_type=dist_type, 
                                       run_clustering=False)

      inst_view = {}
      inst_view['pct_row_' + rank_type] = inst_filt
      inst_view['dist'] = 'cos'
      inst_view['nodes'] = {}
      inst_view['nodes']['row_nodes'] = tmp_net.viz['row_nodes']
      inst_view['nodes']['col_nodes'] = tmp_net.viz['col_nodes']

      all_views.append(inst_view)

    except:
      pass

  return all_views  