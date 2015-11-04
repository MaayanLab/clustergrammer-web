from d3_clustergram_class import Network

net = Network()

# load json 
g2e = net.load_json_to_dict('mock_g2e/failing_clustergrammer_post_data.json')

net.load_g2e_to_net(g2e)

net.swap_nan_for_zero()
net.filter_network_thresh(0.01,2)

net.cluster_row_and_col('cos')