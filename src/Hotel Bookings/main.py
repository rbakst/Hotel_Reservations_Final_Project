from entities.guest import Guest
from entities.reservation import Reservation
import pandas as pd
import sql.create_database as db
import data_analysis.cleaning as cleaning
import data_analysis.visualization as visualization
from map_reduce import map_reduce
import os

def main():
    #needed this once I made it into a package (in order to import from a sibling folder). not sure what the best solution is...
    file_path = os.path.dirname(__file__)+"\\hotel_bookings.csv"
    df_reservations = pd.read_csv(file_path,na_values = "'undefined', ' ', 'none', '-' ")
    
    clean_reservations_dataframe(df_reservations)
    #visualize_reservations_dataframe(df_reservations)
    
        #this is not working b/c gives only values not keys
        #reservations_list=list(map(lambda x:Reservation(x),df_reservations.values.tolist()))
        #unexpected keyword argument 'hotel'
        #reservations_list = [Reservation(**kwargs) for kwargs in df_reservations.to_dict(orient='records')]
        
        #come back to figuring out a more efficient way of doing this
        #reservations_list = [Reservation(row) for row in df_reservations.iterrows()]
        
        #now there is a list of reservation objects with all the necessary fields and we can work with that list.
        # we can insert it into the database.
        #then they can query the data (which will populate the Reservation or Guest objects) and use that data for other purposes.
        #sql.create_database.generate_script(reservations_list[0])
        #switch this back to what's above:
        #sql.create_database.generate_script(Reservation(df_reservations.iloc[0]))
    db.create_tables_from_df(df_reservations)
    df_reservations_filtered = db.query()
    reservations_list = [Reservation(row) for row in df_reservations_filtered.iterrows()]
    #any ideas of what we can do now with a reservation object?


# I think we could tell them to use mapreduce for at least 2 (eg) of these cleanings
def clean_reservations_dataframe(df_reservations):
    # The following function will return information for analysis for a specific dataframe.
    cleaning.analyze_df(df_reservations)
    #updates to datetime or bool type
    cleaning.update_col_datatype(df_reservations,'is_canceled','bool')
    #needs working on
    cleaning.combine_cols(df_reservations ,['arrival_date_year','arrival_date_month','arrival_date_day_of_month'],'arrival_date','datetime')
    #dropes any col with less then 70% of the data
    cleaning.drop_cols_missing_data(df_reservations,70)
    # remove all the rows from the df that dont have a agent
    cleaning.remove_rows_with_missing_value_from_col (df_reservations, 'agent')
    #fills the nans with the mean of the column and then rounds it.
    cleaning.fill_missing_values_with_rounded_mean(df_reservations, 'children')
    
    #fills the nans with the value from the prev row. mapreduce example

    def merge_dfs(df1, df2):
        df1.join(df2)
        return df1
    
    map_reduce(df_reservations, 4, cleaning.fill_missing_values_with_value_from_prev_row, merge_dfs, ['agent', 'country'])

    cleaning.fill_missing_values_with_value_from_prev_row(df_reservations,['agent','country'])

    #this func will convert a col to a set and take in a list it will then lookup what exists in the set.
    cleaning.set_lookup(df_reservations , 'lead_time', [1,567,678,45])

def visualize_reservations_dataframe(df_reservations):
    
    # The following function will create a heatmap for the df
    visualization.create_heatmap_corr(df_reservations)
    # The following function will create a catplot of the count for a number of columns
    #visualization.create_catplot(df_reservations, cols=["arrival_date_month", "market_segment"])
    # The following function will create a catplot with hue.
    #visualization.create_catplot_with_hue(df_reservations, "arrival_date_month", 'hotel', 'month_hotel_catplot.png')
    visualization.create_catplot_with_hue(df_reservations, "market_segment", 'is_canceled', 'market_canceled_catplot.png')
    # The following function will create a catplot of the count for a specific column ,
    # using a filtered dateframe on the top 10 values of this column.
    visualization.create_catplot_top_10(df_reservations, 'country')
    df_reservations['total_guests']= df_reservations['adults']+ df_reservations['children']+ df_reservations['babies']
    # The following function will return the heatmap for the sum of a specific column,
    # grouped by 2 other columns.
    #visualization.create_heatmap_sum_pivot(df_reservations, "arrival_date_month", 'arrival_date_year', 'customers_total')
    df_reservations['total_nights']= df_reservations['stays_in_week_nights']+df_reservations['stays_in_weekend_nights']
    # The following function will create a boxplot for a sepecific column.
    visualization.create_boxplot(df_reservations, cols=['total_nights', 'lead_time'])
    #list comprehension - but may be too complex with the Guest object created inside
    
if __name__ == "__main__":
    main()

