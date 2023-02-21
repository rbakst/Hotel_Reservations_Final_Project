main:

1:52
visualization:
import seaborn as sns
import matplotlib.pyplot as plt
from cleaning import filter_top_10, pivot_sum
# The following function will create a catplot of the count for a number of columns
def create_catplot(df, cols):
    i=0
    for col in cols:
        i+=1
        catplot_name= 'catplot'+ str(i)+ '.png'
        sns.catplot(data=df, x=col, kind= 'count')
        plt.title('Customers/ {}'.format(col))
        plt.xticks(rotation= 90)
        plt.savefig(catplot_name)
        plt.clf()
# The following function will create a catplot with hue.
def catplot_with_hue(df, col, hue_col, catplot_name):
    sns.catplot(data=df, x=col, kind= 'count', hue=hue_col)
    plt.title('Customers/ {}'.format(col))
    plt.xticks(rotation= 90)
    plt.savefig(catplot_name)
    plt.clf()
# The following function will create a boxplot for a sepecific column.
def create_boxplot(df, cols):
    i=0
    for col in cols:
        i+=1
        boxplot_name= 'boxplot'+ str(i)+ '.png'
        sns.boxplot(data= df, x=col)
        plt.savefig(boxplot_name)
        plt.clf()
# The following function will create a catplot of the count for a specific column ,
# using a filtered dateframe on the top 10 values of this column.
def catplot_top_10(df, col):
    filter_10=filter_top_10(df, col)
    sns.catplot(x=col, kind='count', data=filter_10)
    plt.savefig('catplot_top_10.png')
    plt.clf()
# The following function will return the heatmap for the sum of a specific column,
# grouped by 2 other columns.
def heatmap_sum_pivot(df, col_index, col_cols, col_values):
    sum_pivot= pivot_sum(df, col_index, col_cols, col_values)
    sns.heatmap(data=sum_pivot, annot=True, fmt='.1f', linewidths=0.8,  cmap="YlGnBu")
    plt.savefig('heatmap_sum_pivot.png')
    plt.clf()
# The following function will create a heatmap of the correlations.
def heatmap_corr(df):
    plt.figure(figsize=(18, 8))
    sns.heatmap(data= df.corr(), annot=True, cmap='RdYlGn', vmin= -1, vmax= 1)
    plt.savefig('heatmap_corr.png')
    plt.clf()
# The following function will create a lineplot for two columns with a hue and style of two other columns.
def lineplot_hue_style(df, col_x, col_y, col_style, col_hue):
    sns.lineplot(data=df, x=col_x, y= col_y, style= col_style, hue= col_hue)
    plt.xticks(rotation= 90)
    plt.savefig('lineplot_hue_style.png')
    plt.clf()
1:52
cleaning :
import pandas as pd
import numpy as np
#import utils
def reading_in_data_with_nans(df):
    df= pd.read_csv(df,na_values = "'undefined', ' ', 'none', '-' ")
    return df
def df_analysis(df):
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
            #utils.logging.info("dropping column: ") + col
            df.drop(columns=col, inplace=True)
def remove_rows_with_missing_value_from_col(df,column):
    df.dropna(subset=[column],inplace=True)
def filling_missing_values_with_rounded_mean(df,column):
    df[column].fillna(value = df[column].mean(), inplace=True)
    df[column]=df[column].apply(np.floor)
def filling_missing_values_with_value_from_prev_row(df,col_list):
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


# sns.lineplot(data=jan_argentina, x="Date", y="AverageTemperature").set(title='Argentina Yearly Jan Temperature')
# sns.jointplot(x='total_bill', y='tip', data=tips, kind='reg')
# sns.lmplot(x="total_bill", y="tip", hue="smoker", col='time', row='sex', height=3,  data=tips)
# sns.lmplot(x="total_bill", y="big_tip", data=tips,logistic=True)
# sns.heatmap(flights_pivot)
# sns.heatmap(flights_pivot,annot=True, fmt="d",  cmap="YlGnBu")
# sns.catplot(x='day', y='total_bill', kind='bar', data=tips)
# sns.catplot(x='day', hue='sex',kind='count', data=tips) (edited) 

# import pandas as pd
# import numpy as np
# # The following function will return information for analysis for a specific dataframe.
# def df_analysis(df):
#     print(df.head())
#     print(df.info())
#     print(df.isna().sum())
#     print(df.columns)
#     print(df.describe())
# # The following function will print value_counts for a list of columns from a specific df
# def col_value_counts(df, cols):
#     for col in cols:
#         print(df[col].value_counts())
# # The following function will drop unnecessary columns.
# def drop_cols(df, cols):
#     # for col in hotel.columns:
#     # if np.sum(hotel[col].isnull())>(hotel.shape[0]*0.7):
#     #     hotel.drop(columns=col, inplace=True)
#     for col in cols:
#         df= df.drop([col], axis=1)
#     return df
# # The following function will fill NaN's of a specific column with the median.
# def fillna_median(df, col):
#     df[col]= df[col].fillna(df[col].median())
#     return df
# # The following function will filter the df on the top 10 values from a chosen column.
# # The df can later be used to plot/analyze just the top 10 values.
# # (I will use it as an inner function in the plots)
# def filter_top_10(df, col):
#     top_10= df[col].value_counts().sort_values(ascending=False).head(10).keys()
#     filter_10= df[df[col].isin(top_10)]
#     return filter_10
# # The following function will create a pivot table of the sum of the chosen value column
# # with the chosen index, columns. (I will use it as an inner function in the plots)
# def pivot_sum(df, col_index, col_cols, col_values):
#     sum_pivot=df.groupby([col_index, col_cols]).sum().pivot_table(index=col_index,
#             columns=col_cols, values= col_values, aggfunc=np.sum)
#     return sum_pivot
# # The following function will sort the dataframe by the month,
# # so that when we plot our analysis, the months should come up in the correct order.
# def sort_df_month(df, month_col):
#     df[month_col]= pd.Categorical(df[month_col],
#                                     categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
#                                     ordered= True)
#     df.sort_values(month_col, inplace= True)
#     return df
# [12:13 PM] import seaborn as sns


# import matplotlib.pyplot as plt
# from analysis_functions import filter_top_10, pivot_sum
# # The following function will create a catplot of the count for a number of columns
# def create_catplot(df, cols):
#     i=0
#     for col in cols:
#         i+=1
#         catplot_name= 'catplot'+ str(i)+ '.png'
#         sns.catplot(data=df, x=col, kind= 'count')
#         plt.title('Customers/ {}'.format(col))
#         plt.xticks(rotation= 90)
#         plt.savefig(catplot_name)
#         plt.clf()
# # The following function will create a catplot with hue.
# def catplot_with_hue(df, col, hue_col, catplot_name):
#     sns.catplot(data=df, x=col, kind= 'count', hue=hue_col)
#     plt.title('Customers/ {}'.format(col))
#     plt.xticks(rotation= 90)
#     plt.savefig(catplot_name)
#     plt.clf()
# # The following function will create a boxplot for a sepecific column.
# def create_boxplot(df, cols):
#     i=0
#     for col in cols:
#         i+=1
#         boxplot_name= 'boxplot'+ str(i)+ '.png'
#         sns.boxplot(data= df, x=col)
#         plt.savefig(boxplot_name)
#         plt.clf()
# # The following function will create a catplot of the count for a specific column ,
# # using a filtered dateframe on the top 10 values of this column.
# def catplot_top_10(df, col):
#     filter_10=filter_top_10(df, col)
#     sns.catplot(x=col, kind='count', data=filter_10)
#     plt.savefig('catplot_top_10.png')
#     plt.clf()
# # The following function will return the heatmap for the sum of a specific column,
# # grouped by 2 other columns.
# def heatmap_sum_pivot(df, col_index, col_cols, col_values):
#     sum_pivot= pivot_sum(df, col_index, col_cols, col_values)
#     sns.heatmap(data=sum_pivot, annot=True, fmt='.1f', linewidths=0.8,  cmap="YlGnBu")
#     plt.savefig('heatmap_sum_pivot.png')
#     plt.clf()
# # The following function will create a heatmap of the correlations.
# def heatmap_corr(df):
#     plt.figure(figsize=(18, 8))
#     sns.heatmap(data= df.corr(), annot=True, cmap='RdYlGn', vmin= -1, vmax= 1)
#     plt.savefig('heatmap_corr.png')
#     plt.clf()
# # The following function will create a lineplot for two columns with a hue and style of two other columns.
# def lineplot_hue_style(df, col_x, col_y, col_style, col_hue):
#     sns.lineplot(data=df, x=col_x, y= col_y, style= col_style, hue= col_hue)
#     plt.xticks(rotation= 90)
#     plt.savefig('lineplot_hue_style.png')
#     plt.clf()
# [12:13 PM] #import sys
# import pandas as pd
# #import matplotlib.pyplot as plt
# #import seaborn as sns
# #import numpy as np
# from analysis_functions import df_analysis, col_value_counts, drop_cols, fillna_median, sort_df_month
# from plotting_functions import create_catplot, catplot_with_hue, create_boxplot, catplot_top_10, heatmap_sum_pivot, heatmap_corr, lineplot_hue_style
# df=pd.read_csv('C:/Users/praik/Documents/Integralytic/Notebooks/guided-projects/command line/command_line_final_project/hotel_bookings.csv')
# # The following function will return information for analysis for a specific dataframe.
# df_analysis(df)
# # The following function will print value_counts for a list of columns from a specific df
# col_value_counts(df, cols=['country', 'agent', 'company', 'children', 'hotel', 'is_canceled', 'market_segment', 'distribution_channel'])
# # The following function will drop unnecessary columns.
# df= drop_cols(df, cols=['company', 'agent'])
# # The following function will fill NaN's of a specific column with the median.
# df= fillna_median(df, 'children')
# # The following function will sort the dataframe by the month,
# # so that when we plot our analysis, the months should come up in the correct order.
# df= sort_df_month(df, 'arrival_date_month')
# # The following function will create a heatmap of the correlations.
# heatmap_corr(df)
# # The following function will create a catplot of the count for a number of columns
# create_catplot(df, cols=["arrival_date_month", "market_segment"])
# # The following function will create a catplot with hue.
# catplot_with_hue(df, "arrival_date_month", 'hotel', 'month_hotel_catplot.png')
# catplot_with_hue(df, "market_segment", 'is_canceled', 'market_canceled_catplot.png')
# # The following function will create a catplot of the count for a specific column ,
# # using a filtered dateframe on the top 10 values of this column.
# catplot_top_10(df, 'country')
# df['customers_total']= df['adults']+ df['children']+ df['babies']
# # The following function will return the heatmap for the sum of a specific column,
# # grouped by 2 other columns.
# heatmap_sum_pivot(df, "arrival_date_month", 'arrival_date_year', 'customers_total')
# df['stays_total']= df['stays_in_week_nights']+df['stays_in_weekend_nights']
# # The following function will create a boxplot for a sepecific column.
# create_boxplot(df, cols=['stays_total', 'lead_time'])
# TA_TO_bookings= df[df['market_segment'].isin(['Online TA', 'Offline TA/TO'])]
# TA_TO_bookings_mean=TA_TO_bookings.groupby(['arrival_date_month', 'market_segment', 'is_canceled']).sum()
# # The following function will create a lineplot for two columns with a hue and style of two other columns.
# lineplot_hue_style(TA_TO_bookings_mean, "arrival_date_month", 'customers_total', 'market_segment', 'is_canceled')








