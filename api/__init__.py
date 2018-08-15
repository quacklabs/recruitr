
from flask import Blueprint
from flask_graphql import GraphQLView
from core.graphql_engine import schema
from core import db

# from core.models import User
api = Blueprint('api', __name__)
#route graphql endpoints to v2
api.add_url_rule('/v2', view_func=GraphQLView.as_view(
        'v2',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

# view_func = GraphQLView.as_view('graphql', schema=Schema(query=Query), graphiql=True)
# api.add_url_rule('/v2', view_func=view_func)

from . import views



#api.add_url_rule('/v1', methods=["GET","POST","DELETE","PUT"])
