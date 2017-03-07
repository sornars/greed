from .card import CardType, Icons

class Tableau:
    def __init__(self, player_name, cash=0, thugs=None, holdings=None, hand=None):
        self.player_name = player_name
        self._cash = cash
        self.thugs = thugs if thugs else []
        self.holdings = holdings if holdings else []
        self.hand = hand if hand else []

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, value):
        self._set_cash(value)
        if self._cash < 0:
            self._cash = 0

    def _set_cash(self, value):
        self._cash = value

    def draft_card(self, draft_deck):
        draft_card = self.select_option(draft_deck)
        self.hand.append(draft_card)

    def discard_thug(self, game):
        discarded_thug = self.select_option(self.thugs) if self.thugs else None
        if discarded_thug:
            discarded_thug.on_discard(game, self)
        return discarded_thug

    def discard_holding(self, game):
        discarded_holding = self.select_option(self.holdings) if self.holdings else None
        if discarded_holding:
            discarded_holding.on_discard(game, self)
        return discarded_holding

    def pay_cost(self, game, card):
        cost = self.select_option(card.costs, remove_option=False)
        cost_paid = False
        discarded_thugs = []
        discarded_holdings = []
        if (cost.cash <= self.cash and
            cost.thugs <= len(self.thugs) and
            cost.holdings <= len(self.holdings)):
            self.cash -= cost.cash
            for thug in range(cost.thugs):
                discarded_thug = self.discard_thug(game)
                discarded_thugs.append(discarded_thug)
            for holding in range(cost.holdings):
                discarded_holding = self.discard_holding(game)
                discarded_holdings.append(discarded_holding)
            cost_paid = True
        return cost_paid, discarded_thugs, discarded_holdings

    def check_needs(self, needs):
        tableau_icons = self.calculate_icons()
        return True if needs <= tableau_icons else False

    def play_thug(self, game, card):
        self.thugs.append(card)

    def play_holding(self, game, card):
        self.holdings.append(card)
        self.place_markers(card)

    def play_action(self, game, card):
        game.discard_card(self, card)

    def play_card(self, game, card, ignore_costs=False, ignore_needs=False):
        cost_paid = ignore_costs
        needs_met = ignore_needs
        if cost_paid is False:
            cost_paid, discarded_thugs, discarded_holdings = self.pay_cost(game, card)
            for discarded_card in discarded_thugs + discarded_holdings:
                game.discard_card(self, discarded_card)
        if needs_met is False:
            needs_met = self.check_needs(card.needs)
        if cost_paid and needs_met:
            card.when_played(game, self)
            if card.card_type is CardType.THUG:
                self.play_thug(game, card)
            elif card.card_type is CardType.HOLDING:
                self.play_holding(game, card)
            elif card.card_type is CardType.ACTION:
                self.play_action(game, card)
        else:
            # Card discarded without effect
            game.discard_deck.append(card)

    def calculate_icons(self):
        icons = Icons(cash=self.cash, thugs=len(self.thugs), holdings=len(self.holdings))
        for thug in self.thugs:
            icons += thug.icons
        for holding in self.holdings:
            icons += holding.icons
        return icons

    def _calculate_markers(self, card):
        icons = self.calculate_icons() + card.icons
        if card.icons.alcohol == 0:
            icons.alochol = 0
        if card.icons.hearts == 0:
            icons.hearts = 0
        if card.icons.wrenches == 0:
            icons.wrenches = 0
        return icons.alcohol + icons.hearts + icons.wrenches

    def place_markers(self, card):
        total_markers = self._calculate_markers(card)
        card.markers += total_markers
        return total_markers

    def select_option(self, options, remove_option=True):
        if options:
            selected_option = None
            while selected_option is None:
                for index, option in enumerate(options):
                    print(index, option)
                try:
                    selected_option_index = int(input('Please select an option: '))
                except ValueError:
                    selected_option_index = -1
                if selected_option_index in range(len(options)):
                    selected_option = options[selected_option_index]
                    if remove_option:
                        selected_option = options.pop(selected_option_index)
                else:
                    print('Please select a valid option')

            return selected_option
        else:
            raise ValueError('Empty options not allowed')

    def __repr__(self):
        return str({
            'player_name': self.player_name,
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings,
            'hand': self.hand
        })
