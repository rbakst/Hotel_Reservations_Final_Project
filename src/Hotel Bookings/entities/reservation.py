from entities.guest import Guest
from enums.booking_type import Booking_Type
from enums.deposit_type import Deposit_Type
from enums.hotel_type import Hotel_Type
from enums.meal_type import Meal_Type
from enums.reservation_status import Reservation_Status
from enums.room_type import Room_Type
from datetime import datetime

class Reservation:
    def __init__(self, reservation_row):
        #figure out the right way to iterrows. temp fix - set to [1]
        #reservation_row = reservation_row[1]
        #technically can use regex for this
        self.hotel_type = Hotel_Type[reservation_row["hotel"].replace(" ", "_").upper()] #replace space with underscore so will map to enum accurately
        self.lead_days_elapsed = int(reservation_row["lead_time"])
        self.is_canceled = bool(reservation_row["is_canceled"])
        #put this back it's part of cleaning
        #self.arrival_date = reservation_row['arrival_date']#this was not part of original dataset - it's the combined cols from the original dataset
        self.arrival_date_week_num = int(reservation_row["arrival_date_week_number"])
        self.count_weekend_nights = int(reservation_row["stays_in_weekend_nights"])
        self.count_week_nights = int(reservation_row["stays_in_week_nights"])
        self.market_segment = reservation_row["market_segment"]
        self.distribution_channel = reservation_row["distribution_channel"]
        self.is_repeated_guest = bool(reservation_row["is_repeated_guest"])
        self.total_prev_cancellations = int(reservation_row["previous_cancellations"])
        self.total_prev_bookings = int(reservation_row["previous_bookings_not_canceled"])
        self.reserved_room_type = Room_Type[reservation_row["reserved_room_type"].upper()]
        self.assigned_room_type = Room_Type[reservation_row["assigned_room_type"].upper()]
        self.total_booking_changes = int(reservation_row["booking_changes"])
        self.deposit_type = Deposit_Type[reservation_row["deposit_type"].replace(" ", "_").upper()]
        
        self.agent_id = int(reservation_row["agent"]) if reservation_row["agent"] != "nan" else 0 #how to do this in a way they are familiar with
        #waiting for Malka if this should be put back in
        #self.booking_company_id = int(reservation_row["company"])
        self.total_days_in_waiting_list = int(reservation_row["days_in_waiting_list"])
        self.booking_type = Booking_Type[reservation_row["customer_type"].replace("-", "_").upper()]
        self.average_daily_rate = float(reservation_row["adr"])
        self.count_parking_spots = int(reservation_row["required_car_parking_spaces"])
        self.count_special_requests = int(reservation_row["total_of_special_requests"])
        self.last_reservation_status = Reservation_Status[reservation_row["reservation_status"].replace("-","_").upper()]
        self.reservation_status_date_updated = reservation_row["reservation_status_date"]
        self.guest = Guest(reservation_row)

