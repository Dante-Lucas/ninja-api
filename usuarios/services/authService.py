from ninja_jwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class AuthService:

    def authentication(self,**credentials):
        return authenticate(**credentials)

    def generate_token(self,user:any) -> dict:
        try:
            refresh = RefreshToken.for_user(user)
            return {'refresh': str(refresh), 'access': str(refresh.access_token)}
        except Exception as e:
            return {'error':str(e)}
    def blacklist(self,token) -> str:
        try:
            refresh = RefreshToken(token)
            refresh.blacklist()
            return {'success':'Logout realizado com sucesso'}
        except Exception as e:
            print(e) 
        
        