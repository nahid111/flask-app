import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from app_extensions import db


# ===========================================================================================
#                                      Settings Models
# ===========================================================================================

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String(191))
    website_title = db.Column(db.String(191))
    website_email = db.Column(db.String(191))
    address = db.Column(db.Text)
    logo = db.Column(db.String(191))
    favicon = db.Column(db.String(191))


# ===========================================================================================
#                                         Auth Models
# ===========================================================================================
# Here exists Many-to-Many relationship between User and Role
# Here exists Many-to-Many relationship between Role and Permission
# Here exists Many-to-Many relationship between User and Permission


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


permissions_roles = db.Table('permissions_roles',
                             db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer(), db.ForeignKey('permission.id')))


permissions_users = db.Table('permissions_users',
                             db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                             db.Column('permission_id', db.Integer(), db.ForeignKey('permission.id')))


class Permission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    permissions = db.relationship('Permission', secondary=permissions_roles, backref=db.backref('roles', lazy='dynamic'))

    def has_permission(self, permission_name):
        p = Permission.query.filter_by(name=permission_name).first()
        return True if p in self.permissions else False

    def assign_permission(self, permission_name):
        p = Permission.query.filter_by(name=permission_name).first()
        self.roles.append(p)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(191), unique=True)
    password = db.Column(db.String(191))
    username = db.Column(db.String(191))
    full_name = db.Column(db.String(191))
    phone = db.Column(db.String(191))
    avatar = db.Column(db.String(191))
    socketio_session_id = db.Column(db.String(191))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    verified_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    permissions = db.relationship('Permission', secondary=permissions_users, backref=db.backref('users', lazy='dynamic'))

    def get_password_reset_token(self, expires_sec=1800):
        s = Serializer(os.getenv('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def has_role(self, role_name):
        role = Role.query.filter_by(name=role_name).first()
        return True if role in self.roles else False

    def has_permission(self, permission_name):
        p = Permission.query.filter_by(name=permission_name).first()
        if p in self.permissions:
            return True
        for role in self.roles:
            if p in role.permissions:
                return True
        return False

    def assign_role(self, role_name):
        r = Role.query.filter_by(name=role_name).first()
        self.roles.append(r)

    def assign_permission(self, permission_name):
        p = Permission.query.filter_by(name=permission_name).first()
        self.permissions.append(p)

    


