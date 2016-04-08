from flask import Blueprint
from flask.ext.cors import cross_origin

import Enrichr_clustergram_endpoint as enr_clust_endpoint
import vector_upload_endpoint, load_tsv_endpoint, get_viz_json_endpoint

def add_routes(app=None, mongo_address=None):

  upload_pages = Blueprint('upload_pages', __name__, 
    static_url_path='/upload_pages/static', static_folder='./static', 
    template_folder='./templates')

  @upload_pages.route('/clustergrammer/Enrichr_clustergram', methods=['POST','GET'])
  @cross_origin()
  def enrichr_clustergram():
    return enr_clust_endpoint.main(mongo_address)

  @upload_pages.route('/clustergrammer/vector_upload/', methods=['POST'])
  @cross_origin()
  def proc_vector_upload():
    return vector_upload_endpoint.main(mongo_address)

  @upload_pages.route('/clustergrammer/get_viz_json/<user_objid>', methods=['GET'])
  def proc_get_viz_json(user_objid):
    return get_viz_json_endpoint.main(mongo_address, user_objid)

  @upload_pages.route('/clustergrammer/upload_network/', methods=['POST'])
  def upload_network():
    return load_tsv_endpoint.main(mongo_address, response_type='redirect')

  @upload_pages.route('/clustergrammer/matrix_upload/', methods=['POST'])
  def proc_matrix_upload():
    return load_tsv_endpoint.main(mongo_address, response_type='link')

  app.register_blueprint(upload_pages)