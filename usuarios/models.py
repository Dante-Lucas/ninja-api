from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, editable=False,auto_created=True, serialize=False, verbose_name='ID')
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "User"