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
        self.cash = self.cash - card.cost

        tableau_icons = self.calculate_icons()
        if card.needs <= tableau_icons:
            if card.when_played:
                card.when_played(self)
