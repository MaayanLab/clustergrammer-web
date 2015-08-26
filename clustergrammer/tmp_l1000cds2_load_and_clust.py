def main():
  from d3_clustergram_class import Network
 
  # initialize network 
  net = Network()

  # load l1000cds2 json 
  l1000cds2 = net.load_json_to_dict('example_l1000cds2/clsgrm.CD.json')

  # load data into network 
  net.load_l1000cds2(l1000cds2)


main()