# Graphql
[Official Documentation](https://docs.graphene-python.org/projects/django/en/latest/)

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
•	Fragment is type of formatting the piece of code that we will like to reuse in our queries. <br />

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

## Names, variables and directives
### Names

•	For a good practice in graphql, put name for our queries.
•	Where executing we can able to select name of the query which we need to execute.

```graphql
query JustMovies {
  	allMovies{
   		 id
    		title
    		year
  	}
}
query MoviesAndDirectors {
  	allMovies{
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

### Variable

```graphql
query MovieAndDirector($id: Int) {
  	movie(id: $id){
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

Query Variable <br />
```graphql
{
  	"id": 2
}
```

### Directives

```graphql
query MovieAndDirector($id: Int, $showdirector: Boolean= false) {
  	movie(id: $id){
    		id
    		title
    		year
    		director @include(if: $showdirector){
      			name
      			surname
    		}
  	}
}
```

Query Variable <br />
```graphql
{
  	"id": 2,
  	"showdirector": true
}
```

# Mutation
Mutation is to create or update new records.

## Create Mutation

```python
#app/schema.py
class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)       
    movie = graphene.Field(MovieType)
    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)
        return MovieCreateMutation(movie=movie)
class Mutation:
    create_movie = MovieCreateMutation.Field()

#project/schema.py
import graphene
import api.schema
class Query(api.schema.Query, graphene.ObjectType):
    pass
class Mutation(api.schema.Mutation, graphene.ObjectType):
    pass
schema = graphene.Schema(query=Query, mutation=Mutation)
```
<br />

```graphql
mutation CreateMovie{
  	createMovie(title: "text", year: 2020) {
    		movie {
      			id
      			title
      			year
    		}
  	}
}
```

## Update Mutation

```python
#app/schema.py
class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        year = graphene.Int()
        id = graphene.ID(required=True)
    movie = graphene.Field(MovieType)
    def mutate(self, info, id, title, year):
        movie = Movie.objects.get(pk=id)
        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year
        movie.save()            
        return MovieCreateMutation(movie=movie) 
class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
```
<br />

```graphql
mutation UpdateMovie{
  	updateMovie(id: "7", title: "text", year: 2018) {
    		movie {
      			id
      			title
      			year
    		}
  	}
}
```

## Delete Mutation

```python
#app/schema.py
class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True) 
    movie = graphene.Field(MovieType)
    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
       	return MovieDeleteMutation(movie=None)

class Mutation:
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()
```
<br />

```graphql
mutation DeleteMovie{
  	deleteMovie(id: "8") {
    		movie {
      			id
      			title
      			year
    		}
 	}
}
```

## JWT authentication
[Official Documentation](https://django-graphql-jwt.domake.io/en/latest/)

•	Installation
```bash
pip install django-graphql-jwt
```
•	Add AuthenticationMiddleware middleware to your MIDDLEWARE settings:
```python
MIDDLEWARE = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
```
•	Add JSONWebTokenMiddleware middleware to your GRAPHENE settings:
```python
GRAPHENE = {
    'SCHEMA': 'mysite.myschema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
```
•	Add JSONWebTokenBackend backend to your AUTHENTICATION_BACKENDS:
```python
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```
•	In application schema obtain JSON Web Token
```python
import graphql_jwt
class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
```

```graphql
mutation{
  	tokenAuth(username:"admin", password:"admin")
  	{
    		token
  	}
}
```

```json
{
	"data": {
		"tokenAuth": {
			"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTk1MDY4NjY4LCJvcmlnSWF0IjoxNTk1MDY4MzY4fQ.EPbjMEp5bL9sczbmKprU9FivLeIWNvM_iZ5RiEEyJfs"
		}
	}
}
```

## User in context

```python
@login_required
def resolve_all_movies(self, info, **kwargs):
	"""
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication is required')
        """
	return Movie.objects.all()
```

## Authorization

In urls.py

```python
from graphql_jwt.decorators import jwt_cookie
urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', jwt_cookie(GraphQLView.as_view(graphiql=True)))
]
```

```graphql
mutation getToken {
  	tokenAuth(username:"admin", password:"admin")
  	{
    		token
  	}
}
```

```graphql
query fetchAllMovies {
  	allMovies {
    		id
    		title
    		year
  	}
}
```

Once getToken is executed, cookies will save token and we can able to execute fetchAllMovies.

**VerifyToken**

```python
class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
```

```graphql
mutation VerifyToken($token: String)  {
  	verifyToken(token: $token) {
    		payload
  	}
}
```

Query Variable <br />
```graphql
{
  	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTk1MDcxMTE2LCJvcmlnSWF0IjoxNTk1MDcwODE2fQ.ZTZqGF85qtvpCns3PFNyN4r3mGb8pKeVCbw2PoudPdk"
}
```

```json
{
  	"data": {
    		"verifyToken": {
      			"payload": {
        			"username": "admin",
        			"exp": 1595071116,
        			"origIat": 1595070816
      			}
    		}
  	}
}
```

```python
#settings.py

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=5), => Token expired in 5 mins
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7) => Logged out after 7days
    }
```

## Relay
[Official Documentation](https://relay.dev/docs/en/introduction-to-relay)

•	It’s a framework for building data driven applications and it’s powered by graphics. <br />

Need to install django-filter

```batch
pip install django-filter
```

```python
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
#Just For Relay implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = ['title','year']
        interfaces = (relay.Node,)
	
class Query(graphene.ObjectType):
    #all_movies = graphene.List(MovieType)
    all_movies = DjangoFilterConnectionField(MovieNode)
    all_directors = graphene.List(DirectorType)
    movie = graphene.Field(MovieType, id= graphene.Int(),title= graphene.String())
    
   # We don’t need- def resolve_all_movies(self, info, **kwargs):
```

```graphql
query fetchAllMovies {
  	allMovies {
    		edges {
      			node {
       				 id
        				title
        				director {
         					 name
          					surname
        				}
      			}
    		}
  	}
}
```

```json
{
  	"data": {
   		 "allMovies": {
      			"edges": [{
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
        		}]
    		}
  	}
}
```

## Filters

```python
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
                'title': ['exact', 'icontains', 'istartswith'],
                'year': ['exact',]
            }
        interfaces = (relay.Node,)
```

### Exact

```graphql
query fetchAllMovies {
  	allMovies(title: "Titanic") {
    		edges {
      			node {
        			id
        			title
        			director {
          				name
          				surname
        			}
      			}
    		}
  	}
}
```

### IContains

```graphql
query fetchAllMovies {
  	allMovies(title_Icontains: "Ti") {
    		edges {
      			node {
        			id
        			title
        			director {
          				name
          				surname
        			}
      			}
    		}
  	}
}
```

### istartswith

```graphql
query fetchAllMovies {
  	allMovies(title_Istartswith: "Ti") {
    		edges {
      			node {
        			id
        			title
        			director {
          				name
          				surname
        			}
      			}
    		}
  	}
}
```

## Relay Mutation

```python
from graphene import relay
from graphql_relay import from_global_id
class MovieUpdateMutationRelay(relay.ClientIDMutation):
    class Input:
        title = graphene.String()
        id = graphene.ID(required=True)
        
    movie = graphene.Field(MovieType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, title):
        movie = Movie.objects.get(pk=from_global_id(id)[1])
        if title is not None:
            movie.title = title
        movie.save()
                
        return MovieUpdateMutationRelay(movie=movie)
	
class Mutation:
    update_movie_relay = MovieUpdateMutationRelay.Field()
```

```graphql
mutation mutateRelay {
  	updateMovieRelay(
    		input: {
    			id: "TW92aWVOb2RlOjE=",
    			title: "Titanic"
  		}
	) 
	{
    		movie {
      			id
      			title
      			year
    		}
  	}
}
```

```graphql
{
  	"data": {
    		"updateMovieRelay": {
      			"movie": {
        			"id": "1",
        			"title": "Titanic1",
        			"year": 1997
      			}
    		}
  	}
}
```

## Pagination

```graphql
query fetchAllMovies {
	  allMovies(last: 3) {
		    pageInfo {
			      startCursor
			      endCursor
			      hasNextPage
			      hasPreviousPage
		    }
		    edges {
			      node {
					id
					title
					director {
					  name
					  surname
				}
			      }
		    }
	  }
}
```

```json
"pageInfo": {
		"startCursor": "YXJyYXljb25uZWN0aW9uOjM=",
		"endCursor": "YXJyYXljb25uZWN0aW9uOjU=",
		"hasNextPage": false,
		"hasPreviousPage": true
      }
```

```graphql
query fetchAllMovies {
	  allMovies(last: 2) {
		    pageInfo {
			      startCursor
			      endCursor
			      hasNextPage
			      hasPreviousPage
		    }
		    edges {
			      cursor
			      node {
					id
					title
					director {
						  name
						  surname
					}
			      }
		    }
	  }
}
```

```json
{
	  "data": {
		    "allMovies": {
			      "pageInfo": {
					"startCursor": "YXJyYXljb25uZWN0aW9uOjQ=",
					"endCursor": "YXJyYXljb25uZWN0aW9uOjU=",
					"hasNextPage": false,
					"hasPreviousPage": true
			      },
			      "edges": [
					{
						  "cursor": "YXJyYXljb25uZWN0aW9uOjQ=",
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
					  "cursor": "YXJyYXljb25uZWN0aW9uOjU=",
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
query fetchAllMovies {
	  allMovies(last: 2, after: "YXJyYXljb25uZWN0aW9uOjM=") {
		    pageInfo {
			      startCursor
			      endCursor
			      hasNextPage
			      hasPreviousPage
		    }
		    edges {
			      cursor
			      node {
					id
					title
					director {
					  name
					  surname
					}
			      }
		    }
	  }
}
```

```json 
{
	  "data": {
		    "allMovies": {
			      "pageInfo": {
					"startCursor": "YXJyYXljb25uZWN0aW9uOjQ=",
					"endCursor": "YXJyYXljb25uZWN0aW9uOjU=",
					"hasNextPage": false,
					"hasPreviousPage": false
			      },
			      "edges": [
					{
						  "cursor": "YXJyYXljb25uZWN0aW9uOjQ=",
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
						  "cursor": "YXJyYXljb25uZWN0aW9uOjU=",
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

## Schema

It is set of rules for our graphql what kind of operation will accept on our API.

```batch
python manage.py graphql_schema
```

```python
GRAPHENE = {
    'SCHEMA': 'movies.schema.schema',
    'SCHEMA_OUTPUT': 'data/myschema.json', -> Folder to put schema
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}
```
