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
def create_catplot_with_hue(df, col, hue_col, catplot_name):
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
def create_catplot_top_10(df, col):
    filter_10=filter_top_10(df, col)
    sns.catplot(x=col, kind='count', data=filter_10)
    plt.savefig('catplot_top_10.png')
    plt.clf()
# The following function will return the heatmap for the sum of a specific column,
# grouped by 2 other columns.
def create_heatmap_sum_pivot(df, col_index, col_cols, col_values):
    sum_pivot= pivot_sum(df, col_index, col_cols, col_values)
    sns.heatmap(data=sum_pivot, annot=True, fmt='.1f', linewidths=0.8,  cmap="YlGnBu")
    plt.savefig('heatmap_sum_pivot.png')
    plt.clf()
# The following function will create a heatmap of the correlations.
def create_heatmap_corr(df):
    plt.figure(figsize=(18, 8))
    sns.heatmap(data= df.corr(), annot=True, cmap='RdYlGn', vmin= -1, vmax= 1)
    plt.savefig('heatmap_corr.png')
    plt.clf()
# The following function will create a lineplot for two columns with a hue and style of two other columns.
def create_lineplot_hue_style(df, col_x, col_y, col_style, col_hue):
    sns.lineplot(data=df, x=col_x, y= col_y, style= col_style, hue= col_hue)
    plt.xticks(rotation= 90)
    plt.savefig('lineplot_hue_style.png')
    plt.clf()