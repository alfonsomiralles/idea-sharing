import graphene
from graphql_auth import mutations
from graphene_django.types import DjangoObjectType
from users.models import User
from graphql_auth.schema import UserQuery, MeQuery

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(UserQuery, MeQuery, graphene.ObjectType):

    follow_requests = graphene.List(UserType)
    
    def resolve_follow_requests(self, info):
        """
        Retrieve follow requests received by the logged-in user.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user.follow_requests_received.all()
class SendFollowRequest(graphene.Mutation):
    """
    Send a follow request to another user.
    """
    class Arguments:
        username_to_follow = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, username_to_follow: str) -> 'SendFollowRequest':
        """
        Send a follow request.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        try:
            target_user = User.objects.get(username=username_to_follow)
        except User.DoesNotExist:
            raise Exception('User to follow does not exist!')

        # Check if the user is already following the target user
        if target_user in user.following.all():
            raise Exception('You are already following this user!')

        # Check if a follow request has already been sent
        if target_user in user.follow_requests_received.all():
            raise Exception('Follow request already sent!')

        target_user.follow_requests_received.add(user)
        return SendFollowRequest(success=True)

class ApproveFollowRequest(graphene.Mutation):
    """
    Approve a received follow request.
    """
    class Arguments:
        username_to_approve = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, username_to_approve: str) -> 'ApproveFollowRequest':
        """
        Approve a follow request.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        try:
            requester = User.objects.get(username=username_to_approve)
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        if requester not in user.follow_requests_received.all():
            raise Exception('No follow request from this user!')
        
        user.follow_requests_received.remove(requester)
        requester.following.add(user)
        return ApproveFollowRequest(success=True)
    
class DenyFollowRequest(graphene.Mutation):
    """
    Deny a received follow request.
    """
    class Arguments:
        username_to_deny = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, username_to_deny: str) -> 'DenyFollowRequest':
        """
        Deny a follow request.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        try:
            requester = User.objects.get(username=username_to_deny)
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        if requester not in user.follow_requests_received.all():
            raise Exception('No follow request from this user!')

        # Simply remove the requester from the list of received follow requests
        user.follow_requests_received.remove(requester)
        
        return DenyFollowRequest(success=True)    
    
class AuthMutation(graphene.ObjectType):
    """
    Authorization and authentication
    """
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    send_follow_request = SendFollowRequest.Field()
    approve_follow_request = ApproveFollowRequest.Field()
    deny_follow_request = DenyFollowRequest.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()


