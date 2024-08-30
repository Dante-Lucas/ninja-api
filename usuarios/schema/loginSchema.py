from ninja import Schema
from .mixin import UsernameSchemaMixin
class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    refresh: str

class PasswordResetSchema(Schema):
    email: str

class SetPasswordSchema(UsernameSchemaMixin):
    new_password1: str
    new_password2: str
    token: str