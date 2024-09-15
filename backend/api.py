from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from usuarios.controllers import UserController,AuthController
api = NinjaExtraAPI(auth=JWTAuth())
api.register_controllers(UserController,AuthController)

