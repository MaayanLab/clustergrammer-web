from flask import Blueprint, render_template, redirect
import viz_functions as viz_fun

def add_routes(app=None, mongo_address=None):

  viz_page = Blueprint('viz_pages',__name__, static_url_path='/viz_pages/static', 
    static_folder='./static', template_folder='./templates')

  @viz_page.route("/clustergrammer/viz/<user_objid>")
  @viz_page.route("/clustergrammer/viz/<user_objid>/<slug>")
  def viz(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'viz.html')

  @viz_page.route("/clustergrammer/viz_sim_mats/<user_objid>")
  @viz_page.route("/clustergrammer/viz_sim_mats/<user_objid>/<slug>")
  def viz_sim_mats(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'viz_sim_mats.html')

  @viz_page.route("/clustergrammer/Enrichr/<user_objid>")
  @viz_page.route("/clustergrammer/Enrichr/<user_objid>/<slug>")
  def viz_Enrichr(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'Enrichr.html')

  @viz_page.route("/clustergrammer/Enrichr_new/<user_objid>")
  @viz_page.route("/clustergrammer/Enrichr_new/<user_objid>/<slug>")
  def viz_Enrichr_new(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'Enrichr_new.html')    

  @viz_page.route("/clustergrammer/gen3va/<user_objid>")
  @viz_page.route("/clustergrammer/gen3va/<user_objid>/<slug>")
  def viz_gen3va(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'gen3va.html')

  @viz_page.route("/clustergrammer/harmonizome/<user_objid>")
  @viz_page.route("/clustergrammer/harmonizome/<user_objid>/<slug>")
  def viz_harmonizome(user_objid, slug=None):
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'harmonizome.html')

  @viz_page.route("/clustergrammer/l1000cds2/<user_objid>")
  @viz_page.route("/clustergrammer/l1000cds2/<user_objid>/<slug>")
  def viz_l1000cds2(user_objid, slug=None):
    
    net = viz_fun.get_network_from_mongo(user_objid, mongo_address)
    return viz_fun.render_page(net, 'l1000cds2.html')

  app.register_blueprint(viz_page)