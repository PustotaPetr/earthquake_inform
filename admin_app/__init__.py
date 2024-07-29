from flask import app, redirect
from flask_migrate import Migrate
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    current_user,
    login_required,
)
from flask_sqlalchemy import SQLAlchemy

from admin_app.db_model import db
from config import cfg

from .create_app import create_app

flask_app = create_app(db, db_filename=cfg.flask_cfg.db_filename)

migrate = Migrate(flask_app, db)


@login_required
@flask_app.route("/")
def index():
    return redirect("/admin")
