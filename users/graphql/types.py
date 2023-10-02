from graphene_django.types import DjangoObjectType
from users.models import User, Idea

class UserType(DjangoObjectType):
    class Meta:
        model = User

class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea