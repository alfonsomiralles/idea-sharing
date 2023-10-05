import graphene
from graphene_django.types import DjangoObjectType
from users.models import User
from .models import FollowRequest 
from users.schema import UserType
from core.utils import ensure_authenticated

class FollowRequestType(DjangoObjectType):
    class Meta:
        model = FollowRequest

class Query(graphene.ObjectType):
    """
    Query for the followers app.
    """
    follow_requests = graphene.List(FollowRequestType)
    following = graphene.List(UserType)
    followers = graphene.List(UserType)

    def resolve_follow_requests(self, info):
        """
        Retrieve follow requests received by the logged-in user.
        """
        user = info.context.user
        ensure_authenticated(user)
        return FollowRequest.objects.filter(to_user=user)
    
    def resolve_following(self, info):
        """
        Retrieve the list of users that the authenticated user is following.
        """
        user = info.context.user
        ensure_authenticated(user)
        return user.following.all()

    def resolve_followers(self, info):
        """
        Retrieve the list of users that are following the authenticated user.
        """
        user = info.context.user
        ensure_authenticated(user)
        return user.followers.all()

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
        ensure_authenticated(user)
        
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
        ensure_authenticated(user)
        
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
        ensure_authenticated(user)
        
        try:
            requester = User.objects.get(username=username_to_deny)
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        follow_request = FollowRequest.objects.filter(from_user=requester, to_user=user).first()

        if not follow_request:
            raise Exception('No follow request from this user!')

        follow_request.delete()
        return DenyFollowRequest(success=True)   
class UnfollowUser(graphene.Mutation):
    """
    Unfollow another user.
    """
    class Arguments:
        username_to_unfollow = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username_to_unfollow: str) -> 'UnfollowUser':
        """
        Unfollow another user.
        """
        user = info.context.user
        ensure_authenticated(user)

        try:
            target_user = User.objects.get(username=username_to_unfollow)
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        if target_user not in user.following.all():
            return UnfollowUser(success=False, message='You are not following this user')

        user.following.remove(target_user)
        return UnfollowUser(success=True, message='Successfully unfollowed')
    
class RemoveFollower(graphene.Mutation):
    """
    Remove a follower.
    """
    class Arguments:
        username_to_remove = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, username_to_remove: str) -> 'RemoveFollower':
        """
        Remove a follower.
        """
        user = info.context.user
        ensure_authenticated(user)

        try:
            follower = User.objects.get(username=username_to_remove)
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        if follower not in user.followers.all():
            return RemoveFollower(success=False, message='This user is not following you')

        user.followers.remove(follower)
        return RemoveFollower(success=True, message='Successfully removed follower')

class Mutation(graphene.ObjectType):
    send_follow_request = SendFollowRequest.Field()
    approve_follow_request = ApproveFollowRequest.Field()
    deny_follow_request = DenyFollowRequest.Field()
    unfollow_user = UnfollowUser.Field()
    remove_follower = RemoveFollower.Field()
