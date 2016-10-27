import requests

filename = 'example_matrix.txt'
# upload_url = 'http://localhost:9000/clustergrammer/matrix_upload/'
# upload_url = 'http://0.0.0.0:8087/clustergrammer/matrix_upload/'
upload_url = 'http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/'

r = requests.post(upload_url, files={'file': open(filename, 'rb')})

link = r.text

print(link)