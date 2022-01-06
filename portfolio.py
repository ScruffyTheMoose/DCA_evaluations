import yahoo_fin.stock_info as si

class Portfolio:

    def __init__(self, cash: float = 100000) -> None:
        """Constructor for Portfolio instance."""
        
        self.portfolio = {}
        self.cash = cash

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


    def buy(self, symbol: str) -> None:
        """Purchase single share of given symbol."""

        cost = si.get_live_price(symbol)

        if self.cash >= cost:
            self.portfolio[symbol]['shares'] += 1
            self.portfolio[symbol]['cost'] += cost
            self.cash -= cost


    def sell(self, symbol: str) -> None:
        """Sell single share of given symbol."""

        price = si.get_live_price(symbol)

        if symbol in self.portfolio.keys:
            if self.portfolio[symbol]['shares'] >= 1:
                avg_cost = self.portfolio[symbol]['cost'] / self.portfolio[symbol]['shares']
                self.portfolio[symbol]['shares'] -= 1
                self.portfolio[symbol]['cost'] -= avg_cost
                self.cash += price


    def bulk_buy(self, symbol: str, quantity: int) -> None:
        """Update portfolio with new share count and cost after purchase of given quantity of shares."""

        price = si.get_live_price(symbol)
        cost = price * quantity

        if self.cash >= cost:
            self.portfolio[symbol]['shares'] += quantity
            self.portfolio[symbol]['cost'] += cost
            self.cash -= cost


    def sell_bulk(self, symbol: str, quantity: int) -> None:
        """Update portfolio with new share count and cost after selling of given quantity of shares."""

        price = si.get_live_price(symbol)

        if symbol in self.portfolio.keys:
            if self.portfolio[symbol]['shares'] >= quantity:
                avg_cost = self.portfolio[symbol]['cost'] / self.portfolio[symbol]['shares']
                self.portfolio[symbol]['shares'] -= quantity
                self.portfolio[symbol]['cost'] -= avg_cost * quantity
                self.cash += price * quantity


    def balance_portfolio(self, weight: float = .1) -> None:
        """Rebalances the portfolio so that each element of the holdings represents the given weight."""
    
        # checking that weight is possible with size of portfolio
        if weight * len(self.portfolio.keys) > 100:
            return

        weight_cost = (self.cash + self.get_portfolio_value()) * weight

        if weight_cost < 300:
            print('Weight percentage requires too small quantity of cash making rebalancing impossible.')
            return

        need_purchase = []
        complete = []

        for fund in self.portfolio.keys:
            shares = self.get_share_count(fund)
            price = si.get_live_price(fund)
            value = price * shares

            # selling shares until at or below weight_cost
            while value > weight_cost:
                self.sell(fund)
                value = price * (shares - 1)

            # purchasing shares until at or below weight_cost if possible
            while (value + price) <= weight_cost:
                self.buy(fund)
                value = price * (shares + 1)



    def get_portfolio_value(self) -> float:
        """Determine and return the cash value of all elements of the porfolio."""

        total = 0

        for fund in self.portfolio.keys:
            shares = self.portfolio[fund]['shares']
            total += shares * si.get_live_price(fund)

        return total


    def get_share_count(self, symbol: str) -> int:
        """Accessor for share count of symbol."""

        return self.portfolio[symbol]['shares']


    def get_portfolio(self) -> dict:
        """Accessor for portfolio."""

        return self.portfolio


    def get_cash(self) -> float:
        """Accessor for cash."""

        return self.cash