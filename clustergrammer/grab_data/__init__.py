from flask import Blueprint, render_template
from flask.ext.cors import cross_origin

def add_routes(app=None):
  grab_data = Blueprint('grab_data', __name__, static_url_path='/grab_data/static',
    static_folder='./static', template_folder='./templates')

  # @grab_data.route('/clustergrammer/gene_info', methods=['GET'])
  # @cross_origin()
  # def gene_info():
  #   return render_template('help.html')

  @grab_data.route("/clustergrammer/gene_info/<gene_symbol>")
  @cross_origin()
  def gene_info(gene_symbol):
    import requests

    print('imported requests\n*****************')

    base_url = 'http://amp.pharm.mssm.edu/Harmonizome/api/1.0/gene/'

    url = base_url + gene_symbol

    get_response = requests.get(url)

    hzome_info = get_response.text

    return hzome_info


  app.register_blueprint(grab_data)