from ninja_jwt.tokens import RefreshToken,AccessToken
from django.contrib.auth import authenticate

class AuthService:

    def authentication(self,**credentials):
        return authenticate(**credentials)

    def generate_token(self,user):
        try:
            token = AccessToken.for_user(user)
            return {'access': str(token)}
        except Exception as e:
            return {'error':str(e)}
    def blacklist(self,token):
        try:
            refresh = RefreshToken(token)
            refresh.blacklist()
            return {'success':'Logout realizado com sucesso'}
        except Exception as e:
            print(e) 
        
        