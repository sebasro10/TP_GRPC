import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import showtime_pb2
import showtime_pb2_grpc

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def Home(self, request, context):
        return booking_pb2.Message3(message="Welcome to the Booking service!")
    
    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingsByUserID(userid=booking['userid'], dates=booking['dates'])
            
    def GetBookingsByUserID(self, request, context):
        for booking in self.db:
            if str(booking["userid"]) == request.userid:
                return booking_pb2.BookingsByUserID(userid=booking['userid'], dates=booking['dates'])
        return booking_pb2.BookingsByUserID(userid='', dates=[])
                
    def CreateBooking(self, request, context):
        with grpc.insecure_channel('showtime_grpc:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            times = stub.GetTimes(showtime_pb2.Empty2()).schedule
        channel.close()
        
        existsTime = False
        for time in times:
            if str(time.date) == str(request.date):
                if str(request.movieid) in time.movies: existsTime = True
        if not existsTime: return booking_pb2.BookingsByUserID(userid='', dates=[])

        for booking in self.db:
            if str(booking["userid"]) == request.userid:
                for date in booking["dates"]:
                    if str(date["date"]) == request.date:
                        if str(request.movieid) in date["movies"]:
                            return booking_pb2.BookingsByUserID(userid='', dates=[])
                booking["dates"].append({"date":request.date,"movies":[request.movieid]})
                return booking_pb2.BookingsByUserID(userid=booking['userid'], dates=booking['dates'])

        reqBooking = {"dates":[{"date":request.date,"movies":[request.movieid]}],"userid":request.userid}
        self.db.append(reqBooking)
        return booking_pb2.BookingsByUserID(userid=reqBooking['userid'], dates=reqBooking['dates'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
