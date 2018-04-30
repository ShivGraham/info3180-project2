from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect 


app = Flask(__name__)
app.config['SECRET_KEY'] = "Y9%cv'_Sm9u=LAi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wavmilsozcqewx:585eda1d7fca794c6ddb5209d8a1ec616c20ea85819b664fbe361ccd12a3cda8@ec2-54-83-1-94.compute-1.amazonaws.com:5432/dcdkth4ikprp9s'
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
