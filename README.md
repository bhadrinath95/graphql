# Graphql

## Introduction

•	GraphQL is a query language and specification for API.
•	GraphQL is an open source server-side technolog y.
•	This was developed by Facebook to optimize RESTful API calls.
•	It is an execution engine and a data query language.

## Installation

•	pip install graphene_django <br /> 
•	INSTALLED_APPS = [ <br /> 
      ... <br /> 
      'django.contrib.staticfiles', # Required for GraphiQL <br /> 
      'graphene_django' <br /> 
  ] <br /> 
•	# urls.py If have enabled CSRF protection in your Django app you will find that it prevents your API clients from POSTing to the graphql endpoint. <br /> 
  from django.urls import path <br /> 
  from django.views.decorators.csrf import csrf_exempt <br /> 
  from graphene_django.views import GraphQLView <br /> 
  urlpatterns = [ <br /> 
    	path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))), <br /> 
  ] # graphiql=True to graphiql=False if you do not want to use the GraphiQL API browser. <br /> 
•	path('graphql/', GraphQLView.as_view(graphiql=True)) <br /> 
•	settings.py <br /> 
  GRAPHENE = { <br /> 
    	'SCHEMA': 'movies.schema.schema' <br /> 
  } <br /> 
  Where path.schema.schema is the location of the Schema object in your Django project. <br /> 
•	schema.py <br /> 
  import graphene <br /> 
  class Query(graphene.ObjectType): <br /> 
    	pass <br /> 
  schema = graphene.Schema(query=Query) <br /> 

