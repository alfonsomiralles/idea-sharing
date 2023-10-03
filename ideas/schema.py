import graphene
from .models import Idea
from graphene_django.types import DjangoObjectType

class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea

class Query(graphene.ObjectType):
    my_ideas = graphene.List(IdeaType)

    def resolve_my_ideas(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Idea.objects.filter(user=user).order_by('-created_at')
    
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


