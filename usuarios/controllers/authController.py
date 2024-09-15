from ninja_extra import permissions
from django.http import HttpRequest
from django.db.utils import IntegrityError
from ninja_jwt.exceptions import TokenError
from ninja_extra import http_post,http_delete
from ..services import AuthService,UserService
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from ..schema import LoginSchema,TokenSchema,PasswordResetSchema
from usuarios.schema import PasswordResetSchema,SetPasswordSchema
from ninja_extra.controllers import api_controller, ControllerBase


@api_controller('/auth',permissions=[permissions.AllowAny])
class AuthController(ControllerBase):

    def __init__(self, auth:AuthService, user_service:UserService) -> None:
        self.auth = auth
        self.user = user_service

    @http_post('', response={200:dict,400:dict,404:dict, 500:dict},auth=None)    
    def login_user(self,request, user:LoginSchema):
        
        user_exist = self.user.filter(username=user.username)
        if user_exist.exists():
            try: 
                users = self.auth.authentication(**user.dict())
                if users is not None:
                    refresh = self.auth.generate_token(users)
                    return 200,refresh
                return 400,{'error':'Usuário ou senha inválido'}
            except ValidationError:
                return 400,{'error':'Erro de validação dos dados'}
            except IntegrityError:
                return 500,{'error':'Erro interno no sistema'}
        return 404,{'error':'Usuário não encontrado'} 
    @http_post('/reset', response={204:dict,400:dict,500:dict},auth=None)
    def password_reset(self,request,data:PasswordResetSchema):
        form = PasswordResetForm(data.dict())
        try:
            if form.is_valid():
                form.save(request=request)
                return 204,{'message':'Um email foi enviado para vc'}
        except Exception as e:
            return 500,{'error':str(e)}
        return 400,{'error':form.errors}

    @http_post('/reset/confirm',response={204: dict, 400: dict, 500: dict},auth=None)
    def password_reset_confirm(self,request:HttpRequest,data:SetPasswordSchema):
        user_field = self.user_entity.USERNAME_FIELD
        user_data = {user_field: getattr(data,user_field)}
        user = self.user.filter(**user_data)

        if user.exists():
            user = user.get()
            if default_token_generator.check_token(user,data.token):
                user.set_password(data.new_password1)
                user.save()
                return 204,{'message':'Sua senha foi alterada com sucesso'}
        return 400,{'error':'Link inválido'}
    @http_delete('', response={204:dict,401:dict,500:dict},permissions=[permissions.IsAuthenticated])
    def logout_user(self,request, data:TokenSchema):
        try:
            response = self.auth.blacklist(data.refresh)
            return 204,response
        except TokenError:
            return 401,{'error':'O token é inválido ou expirado'}
        except Exception as e:
            return 500,{'error':str(e)}
        
    