# Graphql

## Introduction

•	GraphQL is a query language and specification for API. <br /> 
•	GraphQL is an open source server-side technology. <br /> 
•	This was developed by Facebook to optimize RESTful API calls. <br /> 
•	It is an execution engine and a data query language. <br /> 

## Installation

•	pip install graphene_django <br /> 
```python
INSTALLED_APPS = [
    ...
    'django.contrib.staticfiles', # Required for GraphiQL
    'graphene_django'
]
```
<br />
•	urls.py If have enabled CSRF protection in your Django app you will find that it prevents your API clients from POSTing to the graphql endpoint. <br /> 
<br/>

```python
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
urlpatterns = [
    	path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
] # graphiql=True to graphiql=False if you do not want to use the GraphiQL API browser.
```
<br />

```python
path('graphql/', GraphQLView.as_view(graphiql=True)) 
```

<br /> 
•	settings.py 
<br /> 

```python
GRAPHENE = {
    	'SCHEMA': 'movies.schema.schema'
}
```
<br />
Where path.schema.schema is the location of the Schema object in your Django project.
<br />

•	schema.py 
<br /> 
```python
import graphene
class Query(graphene.ObjectType):
    	pass
schema = graphene.Schema(query=Query)
```

## Schema

•	A GraphQL schema is at the core of any GraphQL server implementation. <br />
•	It describes the functionality available to the client applications that connect to it. <br />
•	Create schema.py to the application. <br />
