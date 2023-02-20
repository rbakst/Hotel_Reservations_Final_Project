from ..entities.guest import Guest
from entities.reservation import Reservation

#this file is intended to be provided to them in order to create the database
def generate_script(first_reservation):
    
    guest = first_reservation.guest
    sql = """create database HotelBookings
            go
            create table Guest
            (GuestId int identity primary key,
            Count_Adults int,
            Count_Children int, 
            Count_Babies int,
            Origin_Country varchar(50)
            )

            create table Reservation
            (

            )"""