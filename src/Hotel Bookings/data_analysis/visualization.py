# import seaborn as sns
# class Visualization:
#     def __init__(self, df):
#         self.df = df


#     #can we make this more complex? add more lines of code? otherwise there's no point in making it a class
#     #similar to the student's code that we saw
#     sns.lineplot(data=jan_argentina, x="Date", y="AverageTemperature").set(title='Argentina Yearly Jan Temperature')
#     sns.jointplot(x='total_bill', y='tip', data=tips, kind='reg')
#     sns.lmplot(x="total_bill", y="tip", hue="smoker", col='time', row='sex', height=3,  data=tips)
#     sns.lmplot(x="total_bill", y="big_tip", data=tips,logistic=True)
#     sns.heatmap(flights_pivot)
#     sns.heatmap(flights_pivot,annot=True, fmt="d",  cmap="YlGnBu")
#     sns.catplot(x='day', y='total_bill', kind='bar', data=tips)
#     sns.catplot(x='day', hue='sex',kind='count', data=tips)