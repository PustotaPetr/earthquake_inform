from flask_sqlalchemy import SQLAlchemy
from .create_app import create_app

db = SQLAlchemy()
flask_app = create_app(db)
