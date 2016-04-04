from flask import Blueprint
from pymongo import MongoClient

def add_routes(app=None, mongo_address=None):

  status_check = Blueprint('status_check', __name__,
    static_url_path='/status_check/static', static_folder='./static',
    template_folder='./templates')

  @status_check.route('/clustergrammer/status_check/<user_objid>', methods=['GET'])
  def status_check_function(user_objid):
    import flask
    from bson.objectid import ObjectId

    # initialize status 
    inst_status = 'error'

    # get object id 
    try:
      obj_id = ObjectId(user_objid)
    except:
      inst_status = 'invalid id'
      return inst_status

    # set up db connection 
    client = MongoClient(mongo_address)
    db = client.clustergrammer

    # find object 
    net = db.networks.find_one({'_id': obj_id })
    client.close()

    # check if processing or error 
    if net['viz'] == 'processing':
      inst_status = 'processing'
    elif net['viz'] == 'error':
      inst_status = 'error'
    elif type(net['viz'] is dict):
      inst_status = 'finished'
      
    return inst_status

  app.register_blueprint(status_check)