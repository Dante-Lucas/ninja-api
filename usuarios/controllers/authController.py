from ninja_extra import http_post
from ..services import AuthService
from ninja_extra import permissions
from django.db.utils import IntegrityError
from ninja_jwt.exceptions import TokenError
from ..schema import LoginSchema,TokenSchema
from django.core.exceptions import ValidationError
from ninja_extra.controllers import api_controller, ControllerBase
@api_controller('/auth')
class AuthController(ControllerBase):

    def __init__(self, auth:AuthService) -> None:
        self.auth = auth

    @http_post('', response={200:dict,400:dict, 500:dict})    
    def login_user(self,request, user:LoginSchema):
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
        
    @http_post('/logout', response={204:dict,401:dict,500:dict},permissions=[permissions.IsAuthenticated])
    def logout_user(self,request, data:TokenSchema):
        try:
            response = self.auth.blacklist(data.refresh)
            return 204,response
        except TokenError:
            return 401,{'error':'O token é inválido ou expirado'}
        except Exception as e:
            return 500,{'error':str(e)}
        
    