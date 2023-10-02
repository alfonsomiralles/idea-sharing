from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Idea(models.Model):
    user = models.ForeignKey(User, related_name='ideas', on_delete=models.CASCADE)
    text = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(
        max_length=10, 
        choices=[('public', 'Public'), ('protected', 'Protected'), ('private', 'Private')], 
        default='public'
    )

    def __str__(self):
        return self.text[:50]

