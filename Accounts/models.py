from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class User(User):
    contact = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.username


