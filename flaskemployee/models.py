from datetime import datetime
from flask import session, abort, request, Response, jsonify
from flaskemployee import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"


class SecureModelView(ModelView):
    def is_accessible(self):
        if 'logged_in' in session:
            return True
        else:
            abort(403)

    column_searchable_list = ['first_name', 'email']


admin.add_view(SecureModelView(User, db.session))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
