from flask import Blueprint, render_template, redirect

def add_routes(app=None):
  home_pages = Blueprint('home_pages', __name__, static_url_path='/home_pages/static',
    static_folder='./static', template_folder='./templates')

  @home_pages.route(app.config['ENTRY_POINT'] + "/")
  def index():
    return render_template('index.html', config=app.config)

  @home_pages.route(app.config['ENTRY_POINT'] + "/case_study_data")
  def case_study_data():
    return render_template('case_study_data.html', config=app.config)

  @home_pages.route(app.config['ENTRY_POINT'] + "/help")
  def help():
    # redirect the user to readthedocs getting started
    return redirect('https://clustergrammer.readthedocs.io/getting_started.html')

  @home_pages.route(app.config['ENTRY_POINT'] + "/CCLE/")
  def ccle():
    # redirect to the updated version of the CCLE explorer
    return redirect('https://maayanlab.github.io/CCLE_Clustergrammer/')


  @home_pages.route(app.config['ENTRY_POINT'] + "/error/<error_desc>")
  def render_error_page(error_desc):
    return render_template('error.html', error_desc=error_desc, config=current_app.config)

  app.register_blueprint(home_pages)
