import graphene
import users.schema as UserSchema
from users.schema import AuthMutation
import ideas.schema as IdeaSchema

class Query(
    UserSchema.Query,
    IdeaSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    AuthMutation,
    IdeaSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
