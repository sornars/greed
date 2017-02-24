from .card import CardType, Icons

class Tableau:
    def __init__(self, cash=0, thugs=None, holdings=None, hand=None, patched_setters=None):
        self.patched_setters = {} if patched_setters is None else patched_setters
        self._cash = cash
        self.thugs = () if thugs is None else thugs
        self.holdings = () if holdings is None else holdings
        self.hand = [] if hand is None else hand

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        if 'cash' in self.patched_setters:
            self._cash = self.patched_setters['cash'](self, value)
        self._cash = value

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

    def play_card(self, card, discarded_cards=None, ignore_costs=False, ignore_needs=False):
        discarded_cards = [] if discarded_cards is None else discarded_cards
        discard_card = True
        if (self._satisfied_needs(card, ignore_needs) and
                self._pay_cost(card, discarded_cards, ignore_costs)):
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

    def select_thug(self):
        # TODO: Implement actual selection
        return self.thugs[-1]

    def select_holding(self):
        # TODO: Implement actual selection
        return self.holdings[-1]

    def _pay_cost(self, card, discarded_cards, ignore_costs):
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
                    chosen_thug = self.select_thug()
                    self.thugs = tuple(thug for thug in self.thugs if thug != chosen_thug)
                    discarded_cards.append(chosen_thug)
                for _ in range(0, cost.holdings):
                    chosen_holding = self.select_holding()
                    self.holdings = tuple(
                        holding for holding in self.holdings if holding != chosen_holding
                    )
                    discarded_cards.append(chosen_holding)
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
