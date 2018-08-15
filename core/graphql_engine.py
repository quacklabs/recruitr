import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import User


class UserModel(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )

class UserConnection(relay.Connection):
    class Meta:
        node = UserModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_users = SQLAlchemyConnectionField(UserConnection)
    # Disable sorting over this field
    #all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

schema = graphene.Schema(query=Query)
