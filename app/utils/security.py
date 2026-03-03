from app import flask_bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Security:
    @staticmethod
    def hash_password(password):
        return flask_bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def check_password_hash(pw_hash, password):
        return flask_bcrypt.check_password_hash(pw_hash, password)

    @staticmethod
    def generate_token(identity):
        return create_access_token(identity=identity, expires_delta=timedelta(days=1))
