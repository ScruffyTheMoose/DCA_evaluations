from portfolio import Portfolio
import pandas as pd
import datetime as dt

# df = pd.read_csv('sector_historical/XLB.csv')

# print(df['Unnamed: 0'].tolist())

# row = df.loc[df['Unnamed: 0'] == '2001-01-02']

portfolio = Portfolio()

print(len(portfolio.portfolio.keys()))

# month = '2001-01-01'
# print(month[5:7])