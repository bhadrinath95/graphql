import graphene 
from graphene_django.types import DjangoObjectType
from .models import Movie, Director
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        
    movie_age = graphene.String()
    
    def resolve_movie_age(self,info):
        return "Old movie" if self.year < 2000 else "New movie"

class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
        
#Just For Relay implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
                'title': ['exact', 'icontains', 'istartswith'],
                'year': ['exact',]
            }
        interfaces = (relay.Node,)
        
class Query(graphene.ObjectType):
    #all_movies = graphene.List(MovieType)
    #movie = graphene.Field(MovieType, id= graphene.Int(),title= graphene.String())
    
    all_movies = DjangoFilterConnectionField(MovieNode)
    all_directors = graphene.List(DirectorType)
    
    movie = relay.Node.Field(MovieNode)
    
    """
    @login_required
    def resolve_all_movies(self, info, **kwargs):
        ""
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication is required')
        ""
        return Movie.objects.all()
    """
    
    def resolve_all_directors(self, info, **kwargs):
        return Director.objects.all()
    
    """
    def resolve_movie(self, info, **kwargs):
        id= kwargs.get('id') 
        title= kwargs.get('title') 
        if id is not None:
            return Movie.objects.get(pk=id)
        
        if title is not None:
            return Movie.objects.get(title=title)
        
        return None
    """
    
class MovieCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)
        
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)
        return MovieCreateMutation(movie=movie)
    
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

class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        
    movie = graphene.Field(MovieType)
    
    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
        return MovieDeleteMutation(movie=None)
    
class Mutation:
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    create_movie = MovieCreateMutation.Field()
    update_movie = MovieUpdateMutation.Field()
    update_movie_relay = MovieUpdateMutationRelay.Field()
    delete_movie = MovieDeleteMutation.Field()
        
        