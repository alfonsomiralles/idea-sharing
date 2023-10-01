import graphene
from graphene_django.types import DjangoObjectType
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "password", "email")

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()
        email = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, email):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return CreateUserMutation(user=user)

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)
    
class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)