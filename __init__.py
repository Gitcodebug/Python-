from flask import Flask, request, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail,Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:tiger@localhost/yuedu'
app.config['SECRET_KEY']= "this is a secruty"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app )
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.yeah.net'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'noreply_reading@yeah.net'
app.config['MAIL_PASSWORD'] = 'qwed12cxza54'
app.config["MAIL_DEFAULT_SENDER"] = '"Flask-User Test" <noreply_readin@yeah.net>'
mail = Mail(app)
from reading import routes