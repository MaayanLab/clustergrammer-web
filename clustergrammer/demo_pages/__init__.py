from flask import Blueprint, render_template
from pymongo import MongoClient
mongo_address = '146.203.54.165'

def add_routes(app=None):
  demo_pages = Blueprint('demo_pages', __name__, static_url_path='/demo_pages/static',
    static_folder='./static', template_folder='./templates')

  @demo_pages.route("/clustergrammer/demo/<user_objid>")
  def demo(user_objid):
    import flask
    from bson.objectid import ObjectId
    from copy import deepcopy

    client = MongoClient(mongo_address)
    db = client.clustergrammer

    try: 
      obj_id = ObjectId(user_objid)
    except:
      error_desc = 'Invalid visualization Id.'
      return redirect('/clustergrammer/error/'+error_desc)

    gnet = db.networks.find_one({'_id': obj_id })

    client.close()

    d3_json = gnet['viz']
    viz_name = gnet['name']

    return render_template('demo.html', viz_network=d3_json, viz_name=viz_name)    

  app.register_blueprint(demo_pages)