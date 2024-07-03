from flask_sqlalchemy import SQLAlchemy
from .create_app import create_app
from config import cfg

db = SQLAlchemy()
flask_app = create_app(db, db_filename=cfg.flask_cfg.db_filename)
