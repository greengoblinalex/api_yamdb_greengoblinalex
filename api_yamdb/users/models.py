from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import ROLES


class User(AbstractUser):
    confirmation_code = models.CharField(max_length=32, editable=False)
    role = models.CharField(choices=ROLES, default='user', max_length=9)
    bio = models.TextField('Biography', blank=True)
