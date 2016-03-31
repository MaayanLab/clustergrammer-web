from flask import Blueprint, render_template
from pymongo import MongoClient
mongo_address = '146.203.54.165'

def add_routes(app=None):
  viz_page = Blueprint('about',__name__, static_url_path='/about/static', static_folder='./static', template_folder='./templates')

  @viz_page.route('/clustergrammer/about')
  def about():
    return render_template('about.html')

  @viz_page.route("/clustergrammer/viz/<user_objid>")
  @viz_page.route("/clustergrammer/viz/<user_objid>/<slug>")
  def viz(user_objid, slug=None):
    import flask
    from bson.objectid import ObjectId

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

    return render_template('viz.html', viz_network=d3_json, viz_name=viz_name)

  @viz_page.route("/clustergrammer/Enrichr/<user_objid>")
  @viz_page.route("/clustergrammer/Enrichr/<user_objid>/<slug>")
  def viz_Enrichr(user_objid, slug=None):
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

    return render_template('Enrichr.html', viz_network=d3_json, viz_name=viz_name)    

  @viz_page.route("/clustergrammer/gen3va/<user_objid>")
  @viz_page.route("/clustergrammer/gen3va/<user_objid>/<slug>")
  def viz_gen3va(user_objid, slug=None):
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

    return render_template('gen3va.html', viz_network=d3_json, viz_name=viz_name)

  @viz_page.route("/clustergrammer/harmonizome/<user_objid>")
  @viz_page.route("/clustergrammer/harmonizome/<user_objid>/<slug>")
  def viz_harmonizome(user_objid, slug=None):
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

    return render_template('harmonizome.html', viz_network=d3_json, viz_name=viz_name)    

  app.register_blueprint(viz_page)