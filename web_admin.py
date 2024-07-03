from admin_app import db, flask_app
from config import cfg


if __name__ == "__main__":
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=True, port=cfg.flask_cfg.port)
