from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect 


app = Flask(__name__)
app.config['SECRET_KEY'] = "Y9%cv'_Sm9u=LAi"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost/photogram"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
app.config['UPLOAD_FOLDER'] = './app/static/uploads'



csrf = CSRFProtect(app) 

#disabling csrf tokens temporarily to test
#WTF_CSRF_ENABLED = False
db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
