import graphene
from .models import Idea
from graphene_django.types import DjangoObjectType
from users.models import User

class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea

class Query(graphene.ObjectType):

    my_ideas = graphene.List(IdeaType)
    user_ideas = graphene.List(IdeaType, username=graphene.String())
    timeline = graphene.List(IdeaType)

    def resolve_my_ideas(self, info):
        """
        Retrieve the list of ideas for the owner user.
        """
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        return Idea.objects.filter(user=user).order_by('-created_at')
    
    def resolve_user_ideas(self, info, username: str):
        """
        Retrieve the list of ideas for a specific user while 
        respecting idea visibility rules.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        try:
            target_user = User.objects.get(username=username)
            
        except User.DoesNotExist:
            raise Exception('User does not exist!')

        is_following = target_user in user.following.all()

        if target_user == user:
            return Idea.objects.filter(user=target_user).order_by('-created_at')
    
        elif is_following:
            return Idea.objects.filter(user=target_user).exclude(
                visibility='private').order_by('-created_at')
    
        else:
            return Idea.objects.filter(
                user=target_user, visibility='public').order_by('-created_at')
         
    def resolve_timeline(self, info):
        """
        Retrieve a timeline of ideas for the authenticated user, 
        including their own ideas and ideas from users they follow.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged in order to view your timeline.')
        
        following_ideas = Idea.objects.filter(
            user__in=user.following.all()
        ).exclude(visibility='private')

        my_ideas = Idea.objects.filter(user=user)
        combined_ideas = my_ideas | following_ideas

        return combined_ideas.order_by('-created_at')

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

class DeleteIdea(graphene.Mutation):
    """
    Delete an existing idea.
    """
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id: int) -> 'DeleteIdea':
        """
        Delete an existing idea associated with the logged-in user.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        try:
            idea = Idea.objects.get(id=id)
        except Idea.DoesNotExist:
            raise Exception('Idea does not exist!')

        if idea.user != user:
            raise Exception('Not authorized!')

        idea.delete()
        return DeleteIdea(success=True)
    
class UpdateIdeaVisibility(graphene.Mutation):
    """
    Update the visibility of an existing idea.
    """
    class Arguments:
        id = graphene.ID(required=True)
        visibility = graphene.String(required=True)

    success = graphene.Boolean()
    idea = graphene.Field(IdeaType)

    def mutate(self, info, id: int, visibility: str) -> 'UpdateIdeaVisibility':
        """
        Update the visibility of an existing idea.
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        
        idea = Idea.objects.get(id=id)
        if idea.user != user:
            raise Exception('Not authorized!')
        
        idea.visibility = visibility
        idea.save()

        return UpdateIdeaVisibility(success=True, idea=idea)

class Mutation(graphene.ObjectType):
    create_idea = CreateIdea.Field()
    update_idea_visibility = UpdateIdeaVisibility.Field()
    delete_idea = DeleteIdea.Field() 


