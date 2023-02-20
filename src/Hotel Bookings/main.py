from entities.guest import Guest
from entities.reservation import Reservation
import pandas as pd
from data_analysis.cleaning import Cleaning
#from data_analysis.visualization import Visualization
import sql.create_database
from data_analysis.cleaning import Cleaning
import os

def main():
    #needed this once I made it into a package (in order to import from a sibling folder). not sure what the best solution is...
    file_path = os.path.dirname(__file__)+"\\hotel_bookings.csv"
    df_hotel_bookings = pd.read_csv(file_path,na_values = "'undefined', ' ', 'none', '-' ")
    #cleaning goes here
    #this is temporary:
    cleaner = Cleaning(df_hotel_bookings)
    cleaner.not_sure_what_these_do()
    reservations_list = []
    
    #list comprehension - but may be too complex with the Guest object created inside 
    reservations_list = [Reservation(row) for row in df_hotel_bookings.iterrows()]
   
    #now there is a list of reservation objects with all the necessary fields and we can work with that list.
    # we can insert it into the database.
    #then they can query the data (which will populate the Reservation or Guest objects) and use that data for other purposes.
    
    #sql.create_database.generate_script(reservations_list[0])
    #switch this back to what's above:
    sql.create_database.generate_script(df_hotel_bookings.iloc[0])

if __name__ == "__main__":
    main()