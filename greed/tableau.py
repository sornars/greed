import abc

from .card import CardType, Icons


class Tableau(abc.ABC):
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
        draft_card, draft_deck = self.select_option(draft_deck, text='Draft card')
        self.hand.append(draft_card)
        return draft_deck

    def discard_thug(self, game):
        discarded_thug, self.thugs = self.select_option(self.thugs, text='Choose THUG to discard') if self.thugs else (None, self.thugs)
        if discarded_thug:
            discarded_thug.on_discard(game, self)
        return discarded_thug

    def discard_holding(self, game):
        discarded_holding, self.holdings = self.select_option(self.holdings,
                                               text='Choose HOLDING to discard') if self.holdings else (None, self.holdings)
        if discarded_holding:
            discarded_holding.on_discard(game, self)
        return discarded_holding

    def pay_cost(self, game, card):
        cost, card.costs = self.select_option(card.costs, remove_option=False, text='Select cost')
        cost_paid = False
        discarded_thugs = []
        discarded_holdings = []
        if (cost.cash <= self.cash and
                cost.thugs <= len(self.thugs) and
                cost.holdings <= len(self.holdings) and
                cost.cards <= len(self.hand)):
            self.cash -= cost.cash
            for _ in range(cost.thugs):
                discarded_thug = self.discard_thug(game)
                discarded_thugs.append(discarded_thug)
            for _ in range(cost.holdings):
                discarded_holding = self.discard_holding(game)
                discarded_holdings.append(discarded_holding)
            for _ in range(cost.cards):
                discarded_card, self.hand = self.select_option(self.hand, text='Choose card to discard')
                game.discard_card(self, discarded_card, on_discard=False)
            cost_paid = True
            for card_paid in discarded_thugs + discarded_holdings:
                card.costs_paid.append(card_paid)
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

    def calculate_markers(self, card):
        icons = self.calculate_icons()
        if card.icons.alcohol == 0:
            icons.alcohol = 0
        if card.icons.hearts == 0:
            icons.hearts = 0
        if card.icons.wrenches == 0:
            icons.wrenches = 0
        return icons.alcohol + icons.hearts + icons.wrenches

    def place_markers(self, card):
        total_markers = self.calculate_markers(card)
        card.markers += total_markers

    @abc.abstractmethod
    def select_option(self, options, remove_option, *args, **kwargs):
        """Take a list of options and return the selected option and the new set of available options"""
        return None, []

    def __repr__(self):
        return str({
            'player_name': self.player_name,
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings,
            'hand': self.hand
        })


class ConsoleTableau(Tableau):

    def select_option(self, options, remove_option=True, text=''):
        if options:
            print(text)
            selected_option = None
            available_options = options[:]
            while selected_option is None:
                more_details = False
                for index, option in enumerate(available_options):
                    print(index, option)
                try:
                    print('Add a question mark (?) for further details on an option')
                    selected_option_index = input(text + ': ')
                    if selected_option_index[-1] == '?':
                        selected_option_index = selected_option_index[:-1]
                        more_details = True
                    selected_option_index = int(selected_option_index)
                except ValueError:
                    selected_option_index = -1
                if selected_option_index in range(len(available_options)):
                    selected_option = available_options[selected_option_index]
                    if more_details:
                        print(repr(selected_option))
                        selected_option = None
                    elif remove_option:
                        selected_option = available_options.pop(selected_option_index)
                else:
                    print('Please select a valid option')

            return selected_option, available_options
        else:
            raise ValueError('Empty options not allowed')
