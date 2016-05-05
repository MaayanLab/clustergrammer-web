from flask import Blueprint, render_template
from pymongo import MongoClient

def add_routes(app=None):
  demo_pages = Blueprint('demo_pages', __name__, static_url_path='/demo_pages/static',
    static_folder='./static', template_folder='./templates')

  @demo_pages.route("/clustergrammer/demo/")
  def demo():
    return render_template('demo.html')

  app.register_blueprint(demo_pages)