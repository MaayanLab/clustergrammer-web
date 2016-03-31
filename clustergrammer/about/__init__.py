from flask import Blueprint, render_template

def add_routes(app=None):
  about_page = Blueprint('about',__name__, static_url_path='/about/static', static_folder='./static', template_folder='./templates')

  @about_page.route('/clustergrammer/about')
  def about():
    return render_template('about.html')

  app.register_blueprint(about_page)