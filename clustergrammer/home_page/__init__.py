from flask import Blueprint, render_template

def add_routes(app=None):
  home_page = Blueprint('home_page', __name__, static_url_path='/home_page/static', 
    static_folder='./static', template_folder='./templates')

  @home_page.route("/clustergrammer/")
  @home_page.route("/Clustergrammer/")
  @home_page.route("/CLUSTERGRAMMER/")
  def index():
    return render_template('index.html')  

  app.register_blueprint(home_page)