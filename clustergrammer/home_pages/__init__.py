from flask import Blueprint, render_template, redirect

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
    # redirect the user to readthedocs getting started
    return redirect('https://clustergrammer.readthedocs.io/getting_started.html')

  @home_pages.route("/clustergrammer/CCLE/")
  @home_pages.route("/Clustergrammer/CCLE/")
  @home_pages.route("/CLUSTERGRAMMER/CCLE/")
  def ccle():
    # return render_template('ccle.html', flask_var='')
    return redirect('https://maayanlab.github.io/CCLE_Clustergrammer/')


  @home_pages.route("/clustergrammer/error/<error_desc>")
  def render_error_page(error_desc):
    return render_template('error.html', error_desc=error_desc)

  app.register_blueprint(home_pages)