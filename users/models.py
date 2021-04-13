from django.contrib.auth.models import AbstractUser
from django.db import models

from risk.models import Company


class CustomUser(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
