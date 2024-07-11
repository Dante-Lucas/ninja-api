from ninja_extra import NinjaExtraAPI
from ninja.renderers import JSONRenderer
from ninja.parser import Parser
from usuarios.api import UserController
from ninja.security import django_auth


api = NinjaExtraAPI(renderer=JSONRenderer(),parser=Parser(),auth=django_auth)
api.register_controllers(UserController)