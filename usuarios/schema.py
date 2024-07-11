from ninja import ModelSchema,Schema
from .models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'email','password']


class LoginSchema(Schema):
    username: str
    password: str