def main():
	import numpy as np

	# a = np.array([[1],[2],[3]])
	a = np.array([1,2,3])

	b = np.array([[2],[3],[4]])

	print(a)
	print(a.reshape(-1,1))

	# t = np.hstack((a.reshape(-1,1,b)))

	# print(t)



def thresh():	
	import numpy as np 

	# find common data above cutoff 
	# input two vectors and a cutoff, 
	# return common elements of the vector that both meet the cutoff value 

	x = np.arange(9)*2
	y = np.arange(9)*0.5

	cutoff = 3

	# apply threshold
	thresh_x, thresh_y = threshold_vect_comparison(x,y, cutoff)

	if len(thresh_x) >= 3:
		print(x)
		print(y)
		print('\n')
		print(thresh_x)
		print(thresh_y)
	else:
		print('not sufficient data')

def threshold_vect_comparison(x, y, cutoff):
	import numpy as np 

	# x vector 
	############
	# this returns a tuple 
	found_tuple = np.where(x >= cutoff)
	# get index array 
	found_index_x = found_tuple[0]

	# y vector 
	############
	# this returns a tuple 
	found_tuple = np.where(y >= cutoff)
	# get index array 
	found_index_y = found_tuple[0]

	# get common intersection 
	found_common = np.intersect1d(found_index_x, found_index_y)

	# apply cutoff 
	thresh_x = x[found_common]
	thresh_y = y[found_common]

	# return the threshold data 
	return thresh_x, thresh_y

# calculate the distance between two vectors if they share at least n overlapping points 
def calc_dist_vectors( i_vect, j_vect, dist_type, min_num_intersect ):

	import numpy
	import math
	import scipy
	# explicitly import subpackage 
	import scipy.spatial

	# convert numpy arrays to lists 
	i_vect = i_vect.tolist()
	j_vect = j_vect.tolist()

	# find the non-zero indicies of i_vect and j_vect 
	meas_i = numpy.nonzero(i_vect)[0]
	meas_j = numpy.nonzero(j_vect)[0]

	# !! this is not a good way of doing this 
	meas_int = numpy.intersect1d(meas_i, meas_j) 

	# print(meas_int)

	# if there is any overlap 
	if len(meas_int) >= min_num_intersect:

		# grab subset of array using indices 
		data_i = [ i_vect[i] for i in meas_int]
		data_j = [ j_vect[i] for i in meas_int]

		# convert lists to arrays
		data_i = numpy.asarray(data_i)
		data_j = numpy.asarray(data_j)

		# calculate the distance between the rows in data_mat
		# scale down the length by the number of comparisons
		if dist_type == 'euclidean':
			inst_dist = numpy.linalg.norm( data_i - data_j )/ len(meas_int) 
		elif dist_type == 'cosine':
			inst_dist = scipy.spatial.distance.cosine(data_i, data_j)
		elif dist_type == 'jaccard':
			# get intersection and union 
			inst_intersection = list(set(meas_i).intersection(meas_j))
			inst_union = list( set(meas_i).union(meas_j) )
			# calculate jaccard distance 
			inst_dist = 1 - float(len(inst_intersection))/len(inst_union)

	# if there are no overlapping measurements, then set inst_dist to 100 
	else:
		inst_dist = 10000 

	# return the distance between two vectors 
	return inst_dist

main()