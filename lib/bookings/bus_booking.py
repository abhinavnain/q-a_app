from .base_booking import BaseBooking
class BusBooking(BaseBooking):
    def __init__(self, booking_request_object ) -> None:
        self.slot = booking_request_object["slot"]  # Datetime
        self.no_of_tickets = booking_request_object["no_of_tickets"]
        self.operator = booking_request_object["operator"]
    def book(self):
        slot = self.find_slots(self.slot, self.operator)
        if slot:
            no_of_ticket_avalaible = self.find_seats()
            if no_of_ticket_avalaible < self.no_of_tickets:
                self.deny_booking()
            self.process_billing()
        else:
            self.deny_booking()