import graphene
from graphql_auth import mutations
from .types import IdeaType
from users.models import Idea

# Custom mutation to create ideas
class CreateIdea(graphene.Mutation):
    """
    Create an idea with optional visibility setting.
    """
    class Arguments:
        text = graphene.String(required=True)
        visibility = graphene.String()

    success = graphene.Boolean()
    idea = graphene.Field(IdeaType)

    def mutate(self, info, text: str, visibility: str = 'public') -> 'CreateIdea':
        """
        Create a new idea and associate it with the logged-in user.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        idea = Idea.objects.create(user=user, text=text, visibility=visibility)
        return CreateIdea(success=True, idea=idea)
        
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

    create_idea = CreateIdea.Field()