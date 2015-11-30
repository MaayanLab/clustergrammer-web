def main():
	import StringIO
	import pandas as pd 

	f = open('from_excel.txt','r')

	tmp = f.read()

	f.close()

	print(tmp)

	buff = StringIO.StringIO(tmp)

	print(buff)

	df = pd.read_table(buff, index_col=0)

	print(df)


def load_buffer():
	import pandas as pd 
	import io
	import StringIO

	# get buffer of file 
	io_buff = io.open('from_excel.txt', mode='r', buffering=-1)

	print(io_buff)
	print(str(io_buff))

	new_buff = str(io_buff)

	# read buffer into pandas dataframe 
	# tmp = pd.read_table(new_buff, index_col=0)
	# print(tmp)

main()