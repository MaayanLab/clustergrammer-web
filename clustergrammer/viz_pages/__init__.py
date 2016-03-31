from flask import Blueprint, render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from copy import deepcopy
mongo_address = '146.203.54.165'

def get_network_from_mongo(user_objid):
  client = MongoClient(mongo_address)
  db = client.clustergrammer

  try: 
    obj_id = ObjectId(user_objid)
  except:
    obj_id = 'error'

  if obj_id != 'error':
    net = db.networks.find_one({'_id': obj_id })
  else:
    net = 'error'

  client.close()

  return net

def render_page(net, page_route):
  if net != 'error':
    return render_template(page_route, viz_network=net['viz'], viz_name=net['name'])
  else:
    error_desc = 'Invalid visualization Id.'
    return redirect('/clustergrammer/error/'+error_desc)  


def add_routes(app=None):


  viz_page = Blueprint('viz_pages',__name__, static_url_path='/viz_pages/static', 
    static_folder='./static', template_folder='./templates')

  @viz_page.route("/clustergrammer/viz/<user_objid>")
  @viz_page.route("/clustergrammer/viz/<user_objid>/<slug>")
  def viz(user_objid, slug=None):

    net = get_network_from_mongo(user_objid)

    return render_page(net, 'viz.html')

  @viz_page.route("/clustergrammer/Enrichr/<user_objid>")
  @viz_page.route("/clustergrammer/Enrichr/<user_objid>/<slug>")
  def viz_Enrichr(user_objid, slug=None):

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

    return render_template('Enrichr.html', viz_network=d3_json, viz_name=viz_name)    

  @viz_page.route("/clustergrammer/gen3va/<user_objid>")
  @viz_page.route("/clustergrammer/gen3va/<user_objid>/<slug>")
  def viz_gen3va(user_objid, slug=None):

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

    return render_template('gen3va.html', viz_network=d3_json, viz_name=viz_name)

  @viz_page.route("/clustergrammer/harmonizome/<user_objid>")
  @viz_page.route("/clustergrammer/harmonizome/<user_objid>/<slug>")
  def viz_harmonizome(user_objid, slug=None):

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

    return render_template('harmonizome.html', viz_network=d3_json, viz_name=viz_name)    

  app.register_blueprint(viz_page)