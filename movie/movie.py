import grpc
from concurrent import futures
import movie_pb2
import movie_pb2_grpc
import json

class MovieServicer(movie_pb2_grpc.MovieServicer):

    def __init__(self):
        with open('{}/data/movies.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["movies"]

    def Home(self, request, context):
        return movie_pb2.Message(message="Welcome to the Movie service!")

    def GetMovieByID(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                print("Movie found!")
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0.0, director="", id="")

    def GetListMovies(self, request, context):
        for movie in self.db:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])

    def GetMovieByTitle(self, request, context):
        for movie in self.db:
            if movie['title'] == request.title:
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0.0, director="", id="")
    
    def CreateMovie(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                return movie_pb2.Message(message="movie ID already exists")
        self.db.append({'title': request.title, 'rating':request.rating,'director':request.director,'id':request.id})
        return movie_pb2.Message(message="movie added")
    
    def UpdateMovieRate(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                movie['rating'] = request.rating
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0.0, director="", id="")

    def DeleteMovie(self, request, context):
        for movie in self.db:
            if movie['id'] == request.id:
                self.db.remove(movie)
                return movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])
        return movie_pb2.MovieData(title="", rating=0.0, director="", id="")

    def GetMoviesByDirector(self, request, context):
        res = []
        for movie in self.db:
            if movie['director'] == request.director:
                res.append(movie)
        
        for movie in res:
            yield movie_pb2.MovieData(title=movie['title'], rating=movie['rating'], director=movie['director'], id=movie['id'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    movie_pb2_grpc.add_MovieServicer_to_server(MovieServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
