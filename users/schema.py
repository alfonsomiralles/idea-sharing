import graphene
from graphql_auth import mutations
from graphene_django.types import DjangoObjectType
from users.models import User
from graphql_auth.schema import UserQuery, MeQuery

class UserType(DjangoObjectType):
    class Meta:
        model = User
class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass  
    
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


