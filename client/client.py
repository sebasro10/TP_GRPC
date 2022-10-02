import grpc

import movie_pb2
import movie_pb2_grpc

def get_movie_by_id(stub,id):
    movie = stub.GetMovieByID(id)
    print(movie)

def get_list_movies(stub):
    allmovies = stub.GetListMovies(movie_pb2.Empty())
    for movie in allmovies:
        print("Movie called %s" % (movie.title))

def get_movie_by_title(stub,title):
    movie = stub.GetMovieByTitle(title)
    print(movie)

def create_movie(stub,newMovie):
    print(stub.CreateMovie(newMovie))

def update_movie_rate(stub,movieRate):
    movie = stub.UpdateMovieRate(movieRate)
    print(movie)

def delete_movie(stub,id):
    movie = stub.DeleteMovie(id)
    print(movie)
    
def get_movies_by_director(stub,director):
    movies = stub.GetMoviesByDirector(director)
    for movie in movies:
        print("Movie called %s" % (movie.title))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        
        print("-------------- Home -----------------------")
        print(stub.Home(movie_pb2.Empty()))

        print("-------------- GetMovieByID ---------------")
        movieid = movie_pb2.MovieID(id="a8034f44-aee4-44cf-b32c-74cf452aaaae")
        get_movie_by_id(stub, movieid)

        print("-------------- GetListMovies --------------")
        get_list_movies(stub)
        
        print("-------------- GetMovieByTitle ------------")
        get_movie_by_title(stub, movie_pb2.MovieTitle(title="The Good Dinosaur"))
        
        print("-------------- CreateMovie ----------------")
        create_movie(stub, movie_pb2.MovieData(title="newTitle",rating=2.0,director="director",id="newId"))
        
        print("-------------- UpdateMovieRate ------------")
        update_movie_rate(stub, movie_pb2.MovieRate(rating=3.0,id="newId"))
        
        print("-------------- DeleteMovie ----------------")
        delete_movie(stub, movie_pb2.MovieID(id="newId"))
        
        print("-------------- GetMoviesByDirector ---------")
        get_movies_by_director(stub, movie_pb2.MovieDirector(director="Peter Sohn"))

    channel.close()

if __name__ == '__main__':
    run()
