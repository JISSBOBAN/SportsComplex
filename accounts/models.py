from django.db import models

class UserProfile(models.Model):
    user_email = models.EmailField(unique=True)