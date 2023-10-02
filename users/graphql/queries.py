import graphene
from graphql_auth.schema import UserQuery, MeQuery
from .types import IdeaType
from users.models import Idea

class Query(UserQuery, MeQuery, graphene.ObjectType):
    my_ideas = graphene.List(IdeaType)

    def resolve_my_ideas(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Idea.objects.filter(user=user).order_by('-created_at')
