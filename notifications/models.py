from django.db import models
from users.models import User
from ideas.models import Idea

class Notification(models.Model):

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, related_name='idea_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
