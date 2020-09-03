import os
try:
  from dotenv import load_dotenv
  load_dotenv()
except:
  pass

MONGODB = os.environ.get('MONGODB', '146.203.54.131')
ORIGIN = os.environ.get('ORIGIN', 'https://amp.pharm.mssm.edu')
ENTRY_POINT = os.environ.get('ENTRY_POINT', '/clustergrammer')
HARMONIZOME_URL = os.environ.get('HARMONIZOME_URL', ORIGIN+'/Harmonizome')
ENRICHR_URL = os.environ.get('ENRICHR_URL', ORIGIN+'/Enrichr')
L1000CDS2_URL = os.environ.get('L1000CDS2_URL', ORIGIN + '/l1000cds2')
GEN3VA_URL = os.environ.get('GEN3VA_URL', ORIGIN + '/gen3va')
