import graphene
import users.schema as UserSchema
from users.schema import AuthMutation
import ideas.schema as IdeaSchema
import followers.schema as FollowersSchema

class Query(
    UserSchema.Query,
    IdeaSchema.Query,
    FollowersSchema.Query,
    graphene.ObjectType
):
    pass

class Mutation(
    AuthMutation,
    IdeaSchema.Mutation,
    FollowersSchema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
