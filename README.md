# Graphql

## Introduction

•	GraphQL is a query language and specification for API.
•	GraphQL is an open source server-side technolog y.
•	This was developed by Facebook to optimize RESTful API calls.
•	It is an execution engine and a data query language.

## Installation

•	pip install graphene_django
•	INSTALLED_APPS = [
      ...
      'django.contrib.staticfiles', # Required for GraphiQL
      'graphene_django'
  ]
•	# urls.py If have enabled CSRF protection in your Django app you will find that it prevents your API clients from POSTing to the graphql endpoint.
  from django.urls import path
  from django.views.decorators.csrf import csrf_exempt
  from graphene_django.views import GraphQLView
  urlpatterns = [
    	path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
  ] # graphiql=True to graphiql=False if you do not want to use the GraphiQL API browser.
•	path('graphql/', GraphQLView.as_view(graphiql=True))
•	settings.py
  GRAPHENE = {
    	'SCHEMA': 'movies.schema.schema'
  }
  Where path.schema.schema is the location of the Schema object in your Django project.
•	schema.py
  import graphene
  class Query(graphene.ObjectType):
    	pass
  schema = graphene.Schema(query=Query)

