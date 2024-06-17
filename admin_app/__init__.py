from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['FLASK_ENV'] = 'development'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bot.db'
    app.config['SECRET_KEY'] = 'anykey'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    
    from .db_model import User

    admin = Admin(app, name='Bot Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))

    return app