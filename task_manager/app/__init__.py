from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resources,Api
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yatre'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# from app  import routes

from app.routes import users_task
from app.user_register import user_register
from app.user_login import user_login

app.register_blueprint(users_task)
app.register_blueprint(user_register)
app.register_blueprint(user_login)