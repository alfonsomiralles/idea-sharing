from django.db import models
from users.models import User

# Create your models here.
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
