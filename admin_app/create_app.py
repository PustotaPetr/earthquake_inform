from flask import Flask, url_for
from flask_security import (
    LoginForm,
    SQLAlchemyUserDatastore,
    Security,
    uia_username_mapper,
)
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, helpers
from flask_security.core import current_user
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, validators

from .views import MyAdminIndexView


def create_app(db: SQLAlchemy, db_filename: str = "bot.db"):
    app = Flask(__name__)

    app.config["FLASK_ENV"] = "development"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
    app.config["SECRET_KEY"] = "anykey"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SECURITY_PASSWORD_SALT"] = "qwerty"
    app.config["SECURITY_USERNAME_ENABLE"] = True
    app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = [
        {"username": {"mapper": uia_username_mapper}}
    ]

    db.init_app(app)

    from .db_model import Admin as UserAdmin, Role, User

    class ExtendedLoginForm(LoginForm):
        pass
        # email = StringField('Username', [validators.InputRequired()])

    user_datastore = SQLAlchemyUserDatastore(db, UserAdmin, Role)
    app.security = Security(app, user_datastore, login_form=ExtendedLoginForm)

    admin = Admin(
        app,
        name="Bot Admin",
        index_view=MyAdminIndexView(),
        base_template="admin/master-extended.html",
        template_mode = 'bootstrap4',
    )
    admin.add_view(ModelView(User, db.session))
    # admin.add_link(MenuLink(name=f'{current_user}(logout)', url='/logout'))

    @app.security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            # admin_view=admin.index_view,
            h=helpers,
            get_url=url_for,
        )

    return app
