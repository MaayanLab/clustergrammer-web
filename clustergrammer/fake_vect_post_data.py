import string
import random
random.seed(10)

def main():
  from clustergrammer import Network
  net = Network()

  row_num = 100
  # make up all names for all data 
  row_names = make_up_names(row_num)

  # initialize vect_post 
  vect_post = {}

  vect_post['title'] = 'Some-Clustergram'
  vect_post['link'] = 'some-link'
  vect_post['columns'] = []

  num_columns = 5

  split = True

  # fraction of rows in each column - 1 means all columns have all rows 
  inst_prob = 1


  # make column data 
  for col_num in range(num_columns):

    inst_col = {}

    col_title = 'Col-' + str( col_num+1 )

    inst_col['col_title'] = col_title
    inst_col['link'] = 'col-link'


    # each column will in general have vector, vector_up, and vector_dn 
    vector = []
    vector_up = []
    vector_dn = []

    # get random subset of row_names 
    vect_rows = get_subset_rows(row_names, inst_prob)

    # generate vectors 
    for inst_row in vect_rows:

      # genrate values 
      ##################

      # add positive/negative values 
      if random.random() > 0.5:
        value_up = 10*random.random()
      else: 
        value_up = 0

      if random.random() > 0.5:
        value_dn = -10*random.random()
      else: 
        value_dn = 0

      value = value_up + value_dn

      # genrate vector component 
      #############################
      vector.append([ inst_row, value ])
      vector_up.append([ inst_row, value_up ])
      vector_dn.append([ inst_row, value_dn ])

    # save to columns 
    inst_col['vector'] = vector

    if split:
      inst_col['vector_up'] = vector_up
      inst_col['vector_dn'] = vector_dn


    # save columns to vect_post
    vect_post['columns'].append(inst_col)

  net.save_dict_to_json(vect_post, 'fake_vect_post.json', indent='indent')

def get_subset_rows(row_names, inst_prob):

  subset_rows = []

  for inst_row in row_names:

    if random.random() > 1-inst_prob:
      subset_rows.append(inst_row)

  return subset_rows


def make_up_names(num_names):

  row_names = []

  for i in range(num_names):
    row_names.append(id_generator(5, "WERJASDFNYUIO"))

  row_names = list(set(row_names))

  return row_names

  
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))
  

main()