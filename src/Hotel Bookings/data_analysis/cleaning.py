import pandas as pd
import numpy as np
import utils

class Cleaning:
    #static - happens only once - test this
    utils.setup_logging()

    def __init__(self, df_to_clean):
        self.df = df_to_clean

    def update_col_datatype(self, col_header, desired_datatype):
        if (desired_datatype == "datetime"):
            self.df[col_header]=pd.to_datetime(self.df[col_header])            

    def combine_cols(self, col_header_list, new_col_name, new_col_datatype, drop_original_cols = True):
        #list comprehension
        self.df[new_col_name] = [self.df[col_header].astype(str) + "/" for col_header in col_header_list] #self.df.arrival_date_year.astype(str)+ '/' + self.df.arrival_date_month.astype(str) + '/' +self.df.arrival_date_day_of_month.astype(str))
        self.update_col_datatype(new_col_name, new_col_datatype)
        if drop_original_cols:
            self.df.drop(columns=col_header_list,inplace=True ,axis=1)

    def drop_cols_missing_data(self, percentage_missing_data):
        for col in self.df.columns:
            if np.sum(self.df[col].isnull())>(self.df.shape[0]*(percentage_missing_data/100)):
                utils.logging.info("dropping column: ") + col #is this the column header?
                self.df.drop(columns=col, inplace=True)

   
    #attn Malka
    def not_sure_what_these_do(self):
        self.df.dropna(subset=['agent'],inplace=True)
        self.df.dropna(subset=['company'],inplace=True)
        ####
        self.df['children'].fillna(value = self.df['children'].mean(), inplace=True)
        self.df['children']=self.df['children'].apply(np.floor)

        ###
        col_list=['agent','country']
        for col in col_list:
            self.df[col].fillna(method='bfill',inplace = True)

        self.df['reservation_status_date']=pd.to_datetime(self.df['reservation_status_date'])
        ###
        self.df_set=set(self.df['lead_time'])

        lead_time=[1,567,678,45]
        for time in lead_time:
            if time in self.df_set:
                print (1 )
            else:
                print (2)
    
    def filling_missing_values_with_rounded_mean(self,column):
        self.df[column].fillna(value = self.df[column].mean(), inplace=True)
        self.df[column]=self.df[column].apply(np.floor)
    def filling_missing_values_with_value_from_prev_row(self,col_list):
        for col in col_list:
            self.df[col].fillna(method='bfill',inplace = True)
    def set_lookup(self,col,lookup_time_list):
        self.df_set=set(self.df[col])
        self.lookup_time_list=lookup_time_list
        for time in lookup_time_list:
            if time in self.df_set:
                print ('Exists')
            else:
                print ('Dosent Exist')







