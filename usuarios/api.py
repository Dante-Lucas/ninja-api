from .models import User
from .schema import UserSchema,LoginSchema
from typing import List
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from ninja import Body
from ninja_extra import http_get,http_post
from ninja_extra.controllers import api_controller,ControllerBase

@api_controller('/user')
class UserController(ControllerBase):
    @http_get("/", response=List[UserSchema])
    def get_users(self,request):
        user = User.objects.all() 
        return user

    @http_post('/',response={201:dict,401:dict, 500:dict})
    def create_user(self,request,user:UserSchema):
        username = user.username
        email = user.email
        password = user.password
        
        if User.objects.filter(username=username,email=email).exists():
            return 401,{'error':'Usuário já existente'}
        try:
            users = User.objects.create_user(username=username, email=email, password=password)
            return 201,{'success':'Usuário criado com sucesso'}
        except IntegrityError:
            return 500,{'error':'Erro interno no sistema'}

    @http_post('/login', response={200:dict, 400:dict})    
    def login_user(self,request, user:LoginSchema):
        username = user.username
        password = user.password
        
        users = authenticate(username=username, password=password)
        if users is not None:
            return 200,{'success':'Login efetuado com sucesso'}
        else:
            return 400,{'error':'Usuário ou senha inválidos'}

    
    