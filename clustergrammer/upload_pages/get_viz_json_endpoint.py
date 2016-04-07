def main(mongo_address, user_objid):
  import json
  import api_response

  viz_doc = api_response.get_viz_doc(mongo_address, user_objid)
  viz_json = json.dumps(viz_doc['viz'])

  return viz_json