from django.db import models
from users.models import User

class FollowRequest(models.Model):
    """
    Represents a follow request between two users.
    """
    from_user = models.ForeignKey(User, related_name='follow_requests_made', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follow_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')