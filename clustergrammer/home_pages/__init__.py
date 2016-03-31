from flask import Blueprint, render_template

def add_routes(app=None):
  home_pages = Blueprint('home_pages', __name__, static_url_path='/home_pages/static', 
    static_folder='./static', template_folder='./templates')

  @home_pages.route("/clustergrammer/")
  @home_pages.route("/Clustergrammer/")
  @home_pages.route("/CLUSTERGRAMMER/")
  def index():
    return render_template('index.html')  

  @home_pages.route("/clustergrammer/help")
  def help():
    return render_template('help.html')      

  @home_pages.route("/clustergrammer/CCLE/")
  @home_pages.route("/Clustergrammer/CCLE/")
  @home_pages.route("/CLUSTERGRAMMER/CCLE/")
  def ccle():
    return render_template('ccle.html', flask_var='')

  app.register_blueprint(home_pages)