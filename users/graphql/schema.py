import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from .mutations import CreateIdea, UpdateIdeaVisibility
from .queries import Query as QueryIdeas

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   password_change = mutations.PasswordChange.Field()
   send_password_reset_email = mutations.SendPasswordResetEmail.Field()
   password_reset = mutations.PasswordReset.Field()

   # django-graphql-jwt inheritances
   token_auth = mutations.ObtainJSONWebToken.Field()
   verify_token = mutations.VerifyToken.Field()
   refresh_token = mutations.RefreshToken.Field()

class Query(QueryIdeas, UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
   create_idea = CreateIdea.Field()
   update_idea_visibility = UpdateIdeaVisibility.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
