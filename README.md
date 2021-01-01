# Graphql

## Introduction

•	GraphQL is a query language and specification for API.
•	GraphQL is an open source server-side technolog y.
•	This was developed by Facebook to optimize RESTful API calls.
•	It is an execution engine and a data query language.

## Installation

•	pip install graphene_django <br /> 
•	INSTALLED_APPS = [ <br /> 
      &nbsp;... <br /> 
      &nbsp;'django.contrib.staticfiles', # Required for GraphiQL <br /> 
      &nbsp;'graphene_django' <br /> 
      &nbsp;] <br /> 
•	# urls.py If have enabled CSRF protection in your Django app you will find that it prevents your API clients from POSTing to the graphql endpoint. <br /> 
      &nbsp;from django.urls import path <br /> 
      &nbsp;from django.views.decorators.csrf import csrf_exempt <br /> 
      &nbsp;from graphene_django.views import GraphQLView <br /> 
      &nbsp;urlpatterns = [ <br /> 
    	      &nbsp;&nbsp;path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))), <br /> 
      &nbsp;] # graphiql=True to graphiql=False if you do not want to use the GraphiQL API browser. <br /> 
•	path('graphql/', GraphQLView.as_view(graphiql=True)) <br /> 
•	settings.py <br /> 
      &nbsp;GRAPHENE = { <br /> 
    	&nbsp;&nbsp;'SCHEMA': 'movies.schema.schema' <br /> 
      &nbsp;} <br /> 
      &nbsp;Where path.schema.schema is the location of the Schema object in your Django project. <br /> 
•	schema.py <br /> 
      &nbsp;import graphene <br /> 
      &nbsp;class Query(graphene.ObjectType): <br /> 
    	      &nbsp;&nbsp;pass <br /> 
      &nbsp;schema = graphene.Schema(query=Query) <br /> 

