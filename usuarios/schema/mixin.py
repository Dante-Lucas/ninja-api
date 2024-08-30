from ninja.orm import create_schema
from django.contrib.auth import get_user_model

User = get_user_model()

UsernameSchemaMixin = create_schema(
    User,
    fields=[User.USERNAME_FIELD]
)