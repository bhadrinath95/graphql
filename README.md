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

```python
import graphene 
from graphene_django.types import DjangoObjectType
from .models import Movie
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()
```
<br/>

•	Add application schema to project schema

```python
import graphene
import api.schema
class Query(api.schema.Query, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query)
```
<br />

## Query

•	Queries are used for getting data from the database. <br />
•	We can get either one single record we can filter the record or we can have all the records. <br />

```graphql
query AllMovies {
	allMovies {
		id
		title
		year
		director	 {
			name
			surname
		}
	}
}
```

```json
{
  	"data": {
    		"allMovies": {
      			"edges": [
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjE=",
            					"title": "Titanic",
            					"director": {
              						"name": "James",
              						"surname": "Cameron"
            					}
          				}
        			},
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjI=",
            					"title": "Avatar",
            					"director": {
              						"name": "James",
              						"surname": "Cameron"
            					}
          				}
        			},
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjM=",
            					"title": "Terminator",
            					"director": {
              						"name": "James",
              						"surname": "Cameron"
            					}
          				}
        			},
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjQ=",
            					"title": "Enthiran",
            					"director": {
              						"name": "Shankar",
              						"surname": "S"
            					}
          				}
        			},
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjU=",
            					"title": "2.O",
            					"director": {
              						"name": "Shankar",
              						"surname": "S"
            					}
          				}
        			},
        			{
          				"node": {
            					"id": "TW92aWVOb2RlOjY=",
            					"title": "I",
            					"director": {
              						"name": "Shankar",
              						"surname": "S"
            					}
          				}
        			}
      			]
    		}
  	}
}
```

```graphql
query {
  	allMovies{
   		id
    		title
   		year
  	}
}
```

```json
{
  	"data": {
    		"allMovies": [
     			{
        			"id": "1",
        			"title": "Titanic",
        			"year": 1997
      			}
    		]
  	}
}
```

```graphql
query fetchAllDirectors {
  	allDirectors {
    		id
    		name
    		surname
 	}	
}
```

```json
{
  	"data": {
    		"allDirectors": [
      			{
        			"id": "1",
        			"name": "James",
        			"surname": "Cameron"
      			},
      			{
        			"id": "2",
        			"name": "Shankar",
        			"surname": "S"
      			}
    		]
  	}
}
```

## Query params

```python
class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id= graphene.Int(),title= graphene.String())
    
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()
    
    def resolve_movie(self, info, **kwargs):
        id= kwargs.get('id') 
        title= kwargs.get('title') 
        if id is not None:
            return Movie.objects.get(pk=id)
        
        if title is not None:
            return Movie.objects.get(title=title)
        
        return None
```

```graphql
query {
  	movie(id: 1) {
    		id
    		title
    		year
  	}
}
```

```graphql
query {
  	movie(id: 1, title: "Titanic") {
    		id
    		title
    		year
  	}
}
```

```json
{
  	"data": {
    		"movie": 
		{
      			"id": "1",
      			"title": "Titanic",
      			"year": 1997
    		}
  	}
}
```

## Custom query fields

```python
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        
    movie_age = graphene.String()
    
    def resolve_movie_age(self,info):
        return "Old movie" if self.year < 2000 else "New movie"
```

```python
class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    def resolve_all_movies(self, info, **kwargs):
    	return Movie.objects.all()
```

```graphql
query {
  	allMovies{
    		id
    		title
    		year
    		movieAge
  	}
}
```

```json
{
  	"data": {
    		"allMovies": [
      			{
        			"id": "1",
        			"title": "Titanic",
        			"year": 1997,
        			"movieAge": "Old movie"
      			},
      			{
        			"id": "2",
        			"title": "Avatar",
        			"year": 2009,
        			"movieAge": "New movie"
      			},
    		]
  	}
}
```

## Multiple models

```python
class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
```

```graphql
query {
  	allMovies{
   		id
    		title
    		year
    		movieAge
    		director {
      			name
      			surname
    		}
  	}
}
```

```json
{
  	"data": {
    		"allMovies": [
      			{
        				"id": "1",
        				"title": "Titanic",
        				"year": 1997,
        				"movieAge": "Old movie",
        				"director": {
          					"name": "James",
          					"surname": "Cameron"
        				}
      			},
      			{
        				"id": "2",
        				"title": "Avatar",
        				"year": 2009,
        				"movieAge": "New movie",
        				"director": {
          					"name": "James",
          					"surname": "Cameron"
        				}
			}
    		]
  	}
}
```

```python
class Query(graphene.ObjectType):
	all_directors = graphene.List(DirectorType)
	def resolve_all_directors(self, info, **kwargs):
		return Director.objects.all()
```

```graphql
query fetchAllDirectors {
  	allDirectors {
    		id
    		name
    		surname
 	}	
}
```

```json
{
  	"data": {
    		"allDirectors": [
      			{
        			"id": "1",
        			"name": "James",
        			"surname": "Cameron"
      			},
      			{
        			"id": "2",
        			"name": "Shankar",
        			"surname": "S"
      			}
    		]
  	}
}
```

## Aliases and fragments

•	movie(id: 1)- Return one movie for us  <br />
•	We need to use Alias to have more than one movie <br />

```graphql
query {
  	firstMovie: movie(id: 1) {
    		id
    		title
    		year
    		director {
      			name
      			surname
    		}
  	}
  	secondMovie: movie(id: 2) {
    		id
   		 title
    		year
    		director {
      			name
      			surname
   		 }
  	}
}
```

```json
{
  	"data": {
    		"firstMovie": {
      			"id": 1,
      			"title": "Titanic",
      			"year": 1997,
      			"director": {
        				"name": "James",
        				"surname": "Cameron"
      			}
    		},
    		"secondMovie": {
      			"id": 2,
      			"title": "Avatar",
      			"year": 2009,
      			"director": {
        				"name": "James",
        				"surname": "Cameron"
      			}
    		}
  	}
}
```
•	Here we use a lot of repetition. <br />
•	We can create one fragment, we can use it in both place. <br />

```graphql
query {
  	firstMovie: movie(id: 1) {
    		...movieData
  	}
  	secondMovie: movie(id: 2) {
   		 ...movieData
  	}
}

fragment movieData on MovieType {
  	id
  	title
  	year
  	movieAge
  	director {
    		name
  		surname
  	}
}
```

