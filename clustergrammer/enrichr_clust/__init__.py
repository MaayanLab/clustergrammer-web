from flask import Blueprint, render_template, request
from flask.ext.cors import cross_origin

import Enrichr_clustergram_endpoint as enr_clust_endpoint

def add_routes(app=None, mongo_address=None):

  print('\n\n\nEnrichr_cluster\n\n\n')

  enrichr_clust = Blueprint('enrichr_clust', __name__, 
    static_url_path='/enrichr_clust/static', static_folder='./static', 
    template_folder='./templates')

  @enrichr_clust.route("/clustergrammer/Enrichr_clustergram", methods=['POST','GET'])
  @cross_origin()
  def enrichr_clustergram():

    return enr_clust_endpoint.main(request, mongo_address)

  app.register_blueprint(enrichr_clust)