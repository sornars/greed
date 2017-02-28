from .card import CardType, Icons

class Tableau:
    def __init__(self, player_name, cash=0, thugs=None, holdings=None, hand=None):
        self.patched_setters = {}
        self.player_name = player_name
        self.cash = cash
        self.thugs = thugs if thugs else []
        self.holdings = holdings if holdings else []
        self.hand = hand if hand else []

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        if 'cash' in self.patched_setters:
            self.patched_setters['cash'](self.cash, value)
        self._cash = value

    def draft_card(self, draft_deck):
        draft_card = self.select_option(draft_deck)
        self.hand.append(draft_card)

    def pay_cost(self, game, costs):
        cost = self.select_option(costs)
        cost_paid = False
        discarded_thugs = []
        discarded_holdings = []
        if (cost.cash <= self.cash and
            cost.thugs <= len(self.thugs) and
            cost.holdings <= len(self.holdings)):
            self.cash -= cost.cash
            for thug in range(cost.thugs):
                discarded_thug = self.select_option(self.thugs)
                discarded_thug.on_discard(game, self)
                discarded_thugs.append(discarded_thug)
            for holding in range(cost.holdings):
                discarded_holding = self.select_option(self.holdings)
                discarded_holding.on_discard(game, self)
                discarded_holdings.append(discarded_holding)
            cost_paid = True
        return cost_paid, discarded_thugs, discarded_holdings

    def check_needs(self, needs):
        tableau_icons = self.calculate_icons()
        return True if needs <= tableau_icons else False

    def play_card(self, game, card):
        cost_paid, discarded_thugs, discarded_holdings = self.pay_cost(game, card.costs)
        for discarded_card in discarded_thugs + discarded_holdings:
            game.discard_card(self, discarded_card)
        needs_met = self.check_needs(card.needs)
        if cost_paid and needs_met:
            card.when_played(game, self)
            if card.card_type is CardType.THUG:
                self.thugs.append(card)
            elif card.card_type is CardType.HOLDING:
                self.place_markers(card)
                self.holdings.append(card)
            else:
                game.discard_card(self, card)
        else:
            # Card discarded without effect
            game.discard_deck.append(card)

    def calculate_icons(self):
        icons = Icons(thugs=len(self.thugs), holdings=len(self.holdings))
        for thug in self.thugs:
            icons += thug.icons
        for holding in self.holdings:
            icons += holding.icons
        return icons

    def place_markers(self, card):
        icons = self.calculate_icons() + card.icons
        total_markers = icons.alcohol + icons.hearts + icons.wrenches
        card.markers = total_markers

    def select_option(self, options):
        selected_option = None
        while selected_option is None:
            for index, option in enumerate(options):
                print(index, option)
            try:
                selected_option_index = int(input('Please select an option'))
            except ValueError:
                selected_option_index = -1
            if selected_option_index in range(len(options)):
                selected_option = options.pop(selected_option_index)
            else:
                print('Please select a valid option')

        return selected_option

    def __repr__(self):
        return str({
            'player_name': self.player_name,
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings,
            'hand': self.hand
        })