from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    follow_requests = models.ManyToManyField(
        "self", symmetrical=False, related_name="follow_requests_received", blank=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    
