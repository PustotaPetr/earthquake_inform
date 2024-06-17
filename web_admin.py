from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from admin_app import db, create_app


if __name__ == '__main__':
    flask_app = create_app()
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True)