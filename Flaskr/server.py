import os

from flask import Flask

#from fastai import *
#from fastai.text import *
#from fastai import basic_train

#export_file_PC = 'Fertigstellungsgrad.pkl'
#export_file_name = 'Ampel.pkl'

#classes_PC = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#classes_Ampel = ['Gelb', 'Grün', 'Rot']
#path = Path(__file__).parent

# load the learner Percentage Complete
#try:
#    learn_PC = load_learner(path, export_file_name_PC)
#except RuntimeError as e:
#    if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
#        print(e)
#        message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#        raise RuntimeError(message)
#    else:
#        raise

# load the learner Ampel
#try:
#    learn_Ampel = load_learner(path, export_file_name_Ampel)
#except RuntimeError as e:
#    if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
#        print(e)
#        message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
#        raise RuntimeError(message)
#    else:
#        raise

"""Create and configure an instance of the Flask application."""
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY='dev',
    # store the database in the instance folder
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# load the instance config, if it exists, when not testing
app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
    
# register the database commands
import db
db.init_app(app)

# apply the blueprints to the app
import auth, wbs
app.register_blueprint(auth.bp)
app.register_blueprint(wbs.bp)

# make url_for('index') == url_for('blog.index')
# in another app, you might define a separate main index here with
# app.route, while giving the blog blueprint a url_prefix, but for
# the tutorial the blog will be the main index
app.add_url_rule('/', endpoint='index')
    

