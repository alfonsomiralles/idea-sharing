from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def has_access_to_idea(self, idea) -> bool:
        """
        Determines if the user has access to the given idea based on its visibility.

        Args:
            idea (Idea): The idea instance to check.

        Returns:
            bool: True if the user has access to the idea, False otherwise.
        """
        if idea.visibility == 'public':
            return True
        elif idea.visibility == 'protected':
            return self.is_following(idea.user)
        elif idea.visibility == 'private':
            return self == idea.user
        return False

    def is_following(self, user) -> bool:
        """
        Determines if the user is following another user.

        Args:
            user (User): The user to check if being followed.

        Returns:
            bool: True if following, False otherwise.
        """
        return user in self.following.all()
    
