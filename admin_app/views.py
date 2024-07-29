from flask import redirect, url_for, request
from flask_admin import AdminIndexView
from flask_security import current_user

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated # This does the trick rendering the view only if the user is authenticated


    def inaccessible_callback(self, name, **kwargs): 
        return redirect(url_for('security.login', next=request.url))