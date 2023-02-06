from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)


class CustomUser(AbstractUser):
    tokenSignature = models.CharField(max_length=255, default="", blank=True)

    # class Meta(AbstractUser.Meta):
    #     swappable = "AUTH_USER_MODEL"
