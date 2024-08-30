from ninja_extra import NinjaExtraAPI
from usuarios.controllers import UserController,AuthController

api = NinjaExtraAPI()
api.register_controllers(UserController,AuthController)

