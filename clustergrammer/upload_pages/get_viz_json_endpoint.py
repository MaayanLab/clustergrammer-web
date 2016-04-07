def main(mongo_address, user_objid):
  import json
  import vector_upload_endpoint

  viz_doc = vector_upload_endpoint.get_viz_doc(mongo_address, user_objid)

  viz_json = json.dumps(viz_doc['viz'])

  return viz_json