import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#
from app.ext.cache import cache
from app.myglobals import cache_expiration
#
db_sqlite = SQLAlchemy(use_native_unicode='utf8')

class MyBaseModel(db_sqlite.Model):
    __abstract__ = True
    id = db_sqlite.Column(db_sqlite.Integer, nullable=False, autoincrement=True, primary_key=True)
    def save(self):
        try:
            db_sqlite.session.add(self)
            db_sqlite.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def delete(self):
        try:
            db_sqlite.session.delete(self)
            db_sqlite.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

class User(UserMixin, MyBaseModel):
    __bind_key__ = 'sqlite_user_user'
    __tablename__ = 'user'
    username = db_sqlite.Column(db_sqlite.String(100), nullable=False, unique=True, index=True)
    _password = db_sqlite.Column(db_sqlite.String(256), nullable=False)
    permission = db_sqlite.Column(db_sqlite.Integer, nullable=False)
    def __init__(self, username, password, permission):
        self.username = username
        self._password = password
        self.permission = permission

    @property
    def password(self):
        raise Exception('password is not accessible')
        # return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password

    def verify_password(self, password):
        return self._password == password

    def generate_auth_token(self, expire=cache_expiration):
        token = uuid.uuid4().hex
        cache.set(token, self.id, timeout=expire)
        #### code for single login restriction ####
        cache.set(str(self.id), token, timeout=expire)
        ########
        return token

    def check_permission(self, permission):
        return self.permission & permission == permission

    @staticmethod
    def verify_auth_token(token):
        try:
            userid = cache.get(token)
        except:
            return None
        if userid is None:
            return None
        return User.query.get(userid)


    @staticmethod
    def seed():
        user1 = User('user1', '123456', 0b01)
        user2 = User('user2', '123456', 0b11)
        seeds = [user1, user2]
        db_sqlite.session.add_all(seeds)
        db_sqlite.session.commit()

