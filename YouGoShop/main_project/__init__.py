from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '55695ec127e7c9c7aa40e51fbc88a28c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///yougoshop.db"
db = SQLAlchemy()
db.init_app(app)
bcrypt = Bcrypt(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:test1234@localhost:3306/project"


#init
login_manager=LoginManager() #初始化Flask-Login
login_manager.init_app(app) #將flask與Flask-Login綁定
login_manager.login_view = 'login' #未登入的使用者要進到需登入的頁面時，送他到login()去
login_manager.login_message = '請登入後繼續!' #續上，要被送走時一併跳出的提示訊息
login_manager.login_message_category = 'warning' #提示訊息種類


