from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(default="img/no_avatar.png", upload_to='uploads/%Y/%m/%d/')

    objects = UserManager()

    def __str__(self):
        return self.username
