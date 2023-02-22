from entities.guest import Guest
from entities.reservation import Reservation
from sql.connect_database import DbCon
import pyodbc

def create_tables_from_df(df_reservations):
     db = DbCon()
     db.Connect()
     db.insert_df(df_reservations, "Reservation")
    
def query():
    sql = "select top 10 * from reservation"
    db = DbCon()
    db.Connect()
    df_result = db.ReadSqlQuery(sql)
    return df_result

#this file is intended to be provided to them in order to create the database

def generate_script(first_reservation):
    
    guest = first_reservation.guest
    
    sql = """create database HotelBookings
            go
            create table Guest
            GuestId int identity primary key,"""
    for attribute in vars(guest): #need to figure out getting the dtype. now it's returning class int64
        sql += attribute + " " + type(vars(guest)[attribute]) + ","

    sql.trim_end(",")
    sql += ")"
    """

            create table Reservation
            (

            )"""