from ..models import User
from asgiref.sync import sync_to_async


class UserService:
    
    def __init__(self,):
        self.user_model = User
        
    def get_all(self):
        return self.user_model.objects.all()

    def create(self,**user):
        return self.user_model.objects.create_user(**user)

    def filter(self,**kwargs):
        return self.user_model.objects.filter(**kwargs)