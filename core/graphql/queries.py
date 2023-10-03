import graphene
from graphql_auth.schema import UserQuery, MeQuery
from .types import IdeaType
from ideas.models import Idea

class Query(UserQuery, MeQuery, graphene.ObjectType):
    """
    Query object types for GraphQL API
    """
    my_ideas = graphene.List(IdeaType)

    def resolve_my_ideas(self, info) -> 'Query':
        """
        Fetches the logged-in user's ideas, ordered by creation date (newest to oldest).
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        return Idea.objects.filter(user=user).order_by('-created_at')
