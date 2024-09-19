from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja import Swagger
from usuarios.controllers import UserController,AuthController
api:NinjaExtraAPI = NinjaExtraAPI(
    auth=JWTAuth(),
    docs_url='/docs',
    docs=Swagger(),
    )
api.register_controllers(UserController,AuthController)

