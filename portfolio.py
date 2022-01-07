# Module for the portfolio object that will be used for testing different Dollar Cost Averaging methods using different approaches to the underlying sectors.

import os
import pandas as pd
import datetime


class Portfolio:

    def __init__(self, cash: float = 100000, start_date = datetime.date(2001, 1, 1), end_date = datetime.date(2021, 1, 1) ) -> None:
        """Constructor for Portfolio instance."""
        
        self.portfolio = dict()
        self.cash = cash
        self.data = self.load_data()
        self.start_date = start_date
        self.end_date = end_date


    def add(self, symbol: str) -> None:
        """Add a symbol to the portfolio at specified share count and cost."""

        # checking for key to prevent overwriting
        if symbol in self.portfolio.keys:
            return

        # writing new element to portfolio
        self.portfolio[symbol] = {
            'shares': 0,
            'cost': 0.00
        }


    def remove(self, symbol: str) -> None:
        """Remove a symbol and its data from the portfolio."""

        try:
            del self.portfolio[symbol]
        except:
            return


    def buy(self, symbol: str, date: str) -> None:
        """Purchase single share of given symbol."""

        cost = self.get_price(symbol, date)

        if self.cash >= cost:
            self.portfolio[symbol]['shares'] += 1
            self.portfolio[symbol]['cost'] += cost
            self.cash -= cost


    def sell(self, symbol: str, date: str) -> None:
        """Sell single share of given symbol."""

        price = self.get_price(symbol, date)

        if symbol in self.portfolio.keys:
            if self.portfolio[symbol]['shares'] >= 1:
                avg_cost = self.portfolio[symbol]['cost'] / self.portfolio[symbol]['shares']
                self.portfolio[symbol]['shares'] -= 1
                self.portfolio[symbol]['cost'] -= avg_cost
                self.cash += price


    def bulk_buy(self, symbol: str, quantity: int, date: str) -> None:
        """Update portfolio with new share count and cost after purchase of given quantity of shares."""

        price = self.get_price(symbol, date)
        cost = price * quantity

        if self.cash >= cost:
            self.portfolio[symbol]['shares'] += quantity
            self.portfolio[symbol]['cost'] += cost
            self.cash -= cost


    def sell_bulk(self, symbol: str, quantity: int, date: str) -> None:
        """Update portfolio with new share count and cost after selling of given quantity of shares."""

        price = self.get_price(symbol, date)

        if symbol in self.portfolio.keys:
            if self.portfolio[symbol]['shares'] >= quantity:
                avg_cost = self.portfolio[symbol]['cost'] / self.portfolio[symbol]['shares']
                self.portfolio[symbol]['shares'] -= quantity
                self.portfolio[symbol]['cost'] -= avg_cost * quantity
                self.cash += price * quantity


    def balance_portfolio(self, weight: float, date: str) -> None:
        """Rebalances the portfolio so that each element of the holdings represents the given weight."""
    
        # checking that weight is possible with size of portfolio
        if weight * len(self.portfolio.keys) > 100:
            return

        # cash value of weight percentage relative to total value of portfolio and cash
        weight_cost = (self.cash + self.get_holdings_value()) * weight

        # highest price stock in portfolio
        min_price = self.find_most_expensive()

        # can we afford to buy atleast 1 share of most expensive stock?
        if weight_cost < min_price:
            print('Weight percentage requires too small quantity of cash making rebalancing impossible.')
            return

        # for tracking holdings that need more shares. They will be done after selling off extra shares to ensure there is enough cash available
        need_purchase = []

        # checking all funds in holdings and selling off shares until weight is met from above
        for fund in self.portfolio.keys:
            shares = self.get_share_count(fund)
            price = self.get_price(fund, date)
            value = price * shares

            # selling shares until at or below weight_cost
            while value > weight_cost:
                self.sell(fund)
                value = price * (shares - 1)

            # if there is room for an additional share, store reference for rehandling
            if (value + price) <= weight_cost:
                need_purchase.append(fund)

        # handling holdings that need additional shares
        for fund in need_purchase:
            shares = self.get_share_count(fund)
            price = self.get_price(fund, date)
            value = price * shares

            while (value + price) <= weight_cost:
                self.buy(fund)
                value = price * (shares + 1)



    def get_holdings_value(self, date: str) -> float:
        """Determine and return the cash value of all holdings in the porfolio."""

        total = 0

        for fund in self.portfolio.keys:
            shares = self.portfolio[fund]['shares']
            total += shares * self.get_price(fund, date)

        return total


    def get_portfolio_value(self) -> float:
        """Returns the total value of the portfolio including cash assets."""

        return self.cash + self.get_holdings_value()


    def find_most_expensive(self, date: str) -> float:
        """Returns the element of the portfolio which has the highest stock price for validating weight ratio."""

        max_price = 0

        for fund in self.portfolio.keys:
            price = self.get_price(fund, date)
            if price > max_price:
                max_price = price

        return max_price


    def get_price(self, symbol: str, date: str) -> float:
        """
        Find and return the historical price of a ticker pulled from stored data.
        Date format: YYYY-MM-DD
        """

        # locating the dataframe is self.data
        df = self.find_data(symbol)
        
        # attempting to locate and return the opening price at the given date
        try:
            row = df.loc(df['Unnamed: 0'] == date)
            return row['open'][0]
        # if price not found, returns -1 as sentinel value
        except:
            print('Could not locate price data at the given date, returning -1...')
            return -1


    def load_data(self) -> dict:
        """Loads the csv type historical price data into a dict of references."""

        data = dict()

        for csv in os.listdir('sector_historical'):
            df = pd.read_csv(f'sector_historical/{csv}')
            name = csv[:4] # remove '.csv'
            data[name] = df # add to data

        return data


    def find_data(self, symbol: str) -> pd.DataFrame:
        """Finds and returns the dataframe for a given symbol in self.data."""

        # linear search for dataframe and return
        for key in self.data.keys:
            if key == symbol:
                return self.data[key]


    def deposit(self, amount: float) -> None:
        """Mutator for cash - Deposit additional funds to the cashstack."""

        self.cash += amount


    def get_share_count(self, symbol: str) -> int:
        """Accessor for share count of symbol."""

        return self.portfolio[symbol]['shares']


    def get_portfolio(self) -> dict:
        """Accessor for portfolio."""

        return self.portfolio


    def get_cash(self) -> float:
        """Accessor for cash."""

        return self.cash