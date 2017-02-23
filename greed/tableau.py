from .card import CardType, Icons

class Tableau:
    def __init__(self, cash=0, thugs=None, holdings=None, hand=None):
        self.notify_players = []
        self.cash = cash
        self.thugs = () if thugs is None else thugs
        self.holdings = () if holdings is None else holdings
        self.hand = [] if hand is None else hand

    def __setattr__(self, name, value):
        # TODO: This could be very inefficient
        if name != 'notify_players':
            for callback in self.notify_players:
                callback(self, name, value)

        super().__setattr__(name, value)


    def calculate_icons(self):
        """Calculate the number of icons in the Tableau"""
        icons = Icons()
        for thug in self.thugs:
            icons += thug.icons

        for holding in self.holdings:
            icons += holding.icons

        icons.thugs = len(self.thugs)
        icons.holdings = len(self.holdings)

        return icons

    def play_card(self, card, ignore_costs=False, ignore_needs=False):
        discard_card = True
        if self._satisfied_needs(card, ignore_needs) and self._pay_cost(card, ignore_costs):
            discard_card = False
            self.place_markers(card)
            if card.card_type is CardType.THUG:
                self.thugs += (card,)
            elif card.card_type is CardType.HOLDING:
                self.holdings += (card,)
            elif card.card_type is CardType.ACTION:
                discard_card = True

        return discard_card

    def place_markers(self, card):
        tableau_icons = self.calculate_icons()
        total_icons = card.icons + tableau_icons
        card.markers += total_icons.alcohol + total_icons.hearts + total_icons.wrenches

    def choose_cost(self, card):
        # TODO: Implement actual selection
        return card.costs[0]

    def choose_thug(self):
        # TODO: Implement actual selection
        return self.thugs[:-1]

    def choose_holding(self):
        # TODO: Implement actual selection
        return self.holdings[:-1]

    def _pay_cost(self, card, ignore_costs):
        cost_paid = False
        if ignore_costs:
            cost_paid = True
        else:
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

    def _satisfied_needs(self, card, ignore_needs):
        needs_satisfied = False
        if ignore_needs:
            needs_satisfied = True
        else:
            needs_satisfied = card.needs <= self.calculate_icons() + card.icons

        return needs_satisfied

    def __repr__(self):
        return str({
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings,
            'hand': self.hand
        })
