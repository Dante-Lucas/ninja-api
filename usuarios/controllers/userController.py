from typing import List
from ..services import UserService
from django.db.utils import IntegrityError
from ninja_extra import http_get,http_post
from ..schema import UserSchema,UserResponseSchema
from django.core.exceptions import ValidationError
from ninja_extra.controllers import api_controller,ControllerBase
from ninja_extra import permissions
@api_controller('/user',permissions=[permissions.AllowAny])
class UserController(ControllerBase):

    def __init__(self, user_service: UserService) -> None:
        self.user = user_service

    @http_get("", response=List[UserResponseSchema])
    def get_users(self,request): 
        user = self.user.get_all()
        return user

    @http_post('',response={201:dict,400:dict, 500:dict})
    def create_user(self,request,user:UserSchema):
        
        users = self.user.filter(username=user.username,email=user.email)
        if users.exists():
            return 400,{'error':'Usuário já existente'}
        try:
            users = self.user.create(**user.dict())
            return 201,{'success':'Usuário criado com sucesso'}
        except ValidationError:
            return 400,{'error':'Erro de validação de dados'}
        except IntegrityError:
            return 500,{'error':'Erro interno no sistema'}

