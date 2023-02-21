from entities.guest import Guest
from entities.reservation import Reservation
import inspect

#this file is intended to be provided to them in order to create the database
def generate_script(first_reservation):
    
    guest = first_reservation.guest
    sql = """create database HotelBookings
            go
            create table Guest
            GuestId int identity primary key,"""
    for attribute in vars(guest):
        sql += attribute + " " + type(vars(guest)[attribute]) + ","

    sql.trim_end(",")
    sql += ")"
    """

            create table Reservation
            (

            )"""