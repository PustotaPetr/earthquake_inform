from flask_security import hash_password
from admin_app import db, flask_app
from config import cfg


if __name__ == "__main__":
    with flask_app.app_context():
        # db.create_all()
        if not flask_app.security.datastore.find_user(username='admin'):
            flask_app.security.datastore.find_or_create_role(
                name="admin", description='this is administrator'
                )
            flask_app.security.datastore.create_user(
                username='admin',
                email='test_mail2@mail_serv.com',
                password=hash_password("password"),
                roles=['admin']
            ) 
            db.session.commit()
    flask_app.run(debug=True, port=cfg.flask_cfg.port, host="0.0.0.0")
