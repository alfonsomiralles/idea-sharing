import graphene
from graphene_django.types import DjangoObjectType
from users.models import User
from .models import FollowRequest 

class FollowRequestType(DjangoObjectType):
    class Meta:
        model = FollowRequest

class Query(graphene.ObjectType):
    """
    Query for the followers app.
    """
    follow_requests = graphene.List(FollowRequestType)

    def resolve_follow_requests(self, info):
        """
        Retrieve follow requests received by the logged-in user.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return FollowRequest.objects.filter(to_user=user)

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

        if FollowRequest.objects.filter(from_user=user, to_user=target_user).exists():
            raise Exception('Follow request already sent!')

        FollowRequest.objects.create(from_user=user, to_user=target_user)
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

        follow_request = FollowRequest.objects.filter(from_user=requester, to_user=user).first()

        if not follow_request:
            raise Exception('No follow request from this user!')
        
        follow_request.delete()
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

        follow_request = FollowRequest.objects.filter(from_user=requester, to_user=user).first()

        if not follow_request:
            raise Exception('No follow request from this user!')

        follow_request.delete()
        return DenyFollowRequest(success=True)   

class Mutation(graphene.ObjectType):
    send_follow_request = SendFollowRequest.Field()
    approve_follow_request = ApproveFollowRequest.Field()
    deny_follow_request = DenyFollowRequest.Field()
