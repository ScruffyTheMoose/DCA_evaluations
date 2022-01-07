import pandas as pd
import datetime as dt

df = pd.read_csv('sector_historical/XLB.csv')

d = dt.date(2007, 1, 1)

row = df.loc[df['Unnamed: 0'] == '2001-01-02']

print(type(row['open'].values[0]))