from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Idea
from notifications.models import Notification
from django.core.mail import send_mail

@receiver(post_save, sender=Idea)
def new_idea_notification(sender, instance, created, **kwargs):
    """
    Send notification to followers when a new idea is posted.
    """
    if created:
        idea = instance
        followers = idea.user.followers.all()
        for follower in followers:
            if follower.has_access_to_idea(idea):
                Notification.objects.create(user=follower, idea=idea)

                subject = f'New idea posted by {idea.user.username}'
                message = f'Check out the new idea posted by {idea.user.username}: {idea.text}'
                from_email = 'noreply@ideasharing.com'
                recipient_list = [follower.email]
                
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)