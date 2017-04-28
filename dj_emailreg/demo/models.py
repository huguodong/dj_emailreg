from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    pwd = models.CharField(max_length=30)
    email=models.EmailField()
    is_active = models.BooleanField(default=False)
