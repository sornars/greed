from . import Icons

class Tableau:
    def __init__(self, cash=0, thugs=None, holdings=None, hand=None):
        self.cash = cash
        self.thugs = [] if thugs is None else thugs
        self.holdings = [] if holdings is None else holdings
        self.hand = [] if hand is None else hand

    def calculate_icons(self):
        """Calculate the number of icons in the Tableau"""
        guns = 0
        cars = 0
        keys = 0
        alcohol = 0
        hearts = 0
        wrenches = 0
        for thug in self.thugs:
            guns += thug.icons.guns
            cars += thug.icons.cars
            keys += thug.icons.keys

        for holding in self.holdings:
            alcohol += holding.icons.alcohol
            hearts += holding.icons.hearts
            wrenches += holding.icons.wrenches

        return Icons(guns, cars, keys, alcohol, hearts, wrenches)

    def play_card(self, card):
        cost_paid = self.pay_cost(card)
        if cost_paid:
            tableau_icons = self.calculate_icons()
            if card.needs <= tableau_icons:
                if card.when_played:
                    card.when_played(self)

    def choose_cost(self, card):
        # TODO: Implement actual selection
        return card.costs.pop()

    def choose_thug(self):
        # TODO: Implement actual selection
        return self.thugs[:-1]

    def choose_holding(self):
        # TODO: Implement actual selection
        return self.holdings[:-1]

    def pay_cost(self, card):
        cost_paid = False
        cost = self.choose_cost(card)
        if (cost.cash <= self.cash and
                cost.thugs <= len(self.thugs) and
                cost.holdings <= len(self.holdings)):
            self.cash = self.cash - cost.cash
            for _ in range(0, cost.thugs):
                self.thugs = self.choose_thug()
            for _ in range(0, cost.holdings):
                self.holdings = self.choose_holding()
            cost_paid = True

        return cost_paid


