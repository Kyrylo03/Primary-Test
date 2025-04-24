from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, TestResult
from flask_login import current_user
from flask_admin import expose
from flask_admin.base import AdminIndexView

class MyModelView(ModelView):
    def is_accessible(self):
        # Наприклад, дозволити лише користувачу з ім'ям "admin"
        return current_user.is_authenticated and current_user.username == "admin"

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or current_user.username != 'admin':
            return self.render('admin/no_access.html')
        return super(MyAdminIndexView, self).index()

def init_admin(app):
    admin = Admin(app, name='Адмін-панель', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(TestResult, db.session))