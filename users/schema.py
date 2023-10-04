import graphene
from graphql_auth import mutations
from graphene_django.types import DjangoObjectType
from users.models import User
from django.db.models import Q
from graphql_auth.schema import UserQuery, MeQuery

class UserType(DjangoObjectType):
    class Meta:
        model = User
class Query(UserQuery, MeQuery, graphene.ObjectType):

    search_users = graphene.List(UserType, search_text=graphene.String())

    def resolve_search_users(self, info, search_text: str):
        """
        Search for users by their username, or part of it.
        
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to search for users.')
        
        return User.objects.filter(Q(username__icontains=search_text))
    
class AuthMutation(graphene.ObjectType):
    """
    Authorization and authentication
    """
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()


