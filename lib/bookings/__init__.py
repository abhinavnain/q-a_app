from .bus_booking import BusBooking
class Bookings:
    def __init__(self, booking_request_details):
        if booking_request_details['category_option'] == 'Bus':
            BusBooking(booking_request_details).book()