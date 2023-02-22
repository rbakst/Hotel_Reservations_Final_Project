import pandas as pd
import numpy as np
import utils
def read_in_data_with_nans(df):
    df= pd.read_csv(df,na_values = "'undefined', ' ', 'none', '-' ")
    return df
def analyze_df(df):
    print(df.head())
    print(df.info())
    print(df.isna().sum())
    print(df.columns)
    print(df.describe())
def update_col_datatype(df, col_header, desired_datatype):
    if (desired_datatype == "datetime"):
        df[col_header]=pd.to_datetime(df[col_header])
    elif (desired_datatype == "bool"):
        df[col_header]=df[col_header].astype('bool')
def combine_cols( df,col_header_list, new_col_name, new_col_datatype, drop_original_cols = True):
    #list comprehension
    #df[new_col_name] = [df[col_header].astype(str) + "/" for col_header in col_header_list]
    df[new_col_name] =df.arrival_date_year.astype(str)+ '/' + df.arrival_date_month.astype(str) + '/' +df.arrival_date_day_of_month.astype(str)
    update_col_datatype(df,new_col_name, new_col_datatype)
    if drop_original_cols:
        df.drop(columns=col_header_list,inplace=True ,axis=1)
def drop_cols_missing_data(df, percentage_missing_data):
    for col in df.columns:
        if np.sum(df[col].isnull())>(df.shape[0]*(percentage_missing_data/100)):
            utils.setup_logging() #find a better place to put this - see if it's needed in every file that uses loggings or only once per running of the application
            utils.logging.info("dropping column: " + col) 
            df.drop(columns=col, inplace=True)
def remove_rows_with_missing_value_from_col(df,column):
    df.dropna(subset=[column],inplace=True)
def fill_missing_values_with_rounded_mean(df,column):
    df[column].fillna(value = df[column].mean(), inplace=True)
    df[column]=df[column].apply(np.floor)
def fill_missing_values_with_value_from_prev_row(df,col_list):
    for col in col_list:
        df[col].fillna(method='bfill',inplace = True)
def pivot_sum(df, col_index, col_cols, col_values):
    sum_pivot=df.groupby([col_index, col_cols]).sum().pivot_table(index=col_index,
        columns=col_cols, values= col_values, aggfunc=np.sum)
    return sum_pivot
def filter_top_10(df, col):
    top_10= df[col].value_counts().sort_values(ascending=False).head(10).keys()
    filter_10= df[df[col].isin(top_10)]
    return filter_10
def set_lookup(df,col,lookup_list):
    df_set=set(df[col])
    for time in lookup_list:
        if time in df_set:
            print ('Exists')
        else:
            print ('Dosent Exist')