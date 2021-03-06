import enum

class Card:
    def __init__(self, card_type, priority, name, rules_text='', costs=None, needs=None, icons=None):
        if card_type not in CardType:
            raise ValueError('Invalid card_type')
        self.card_type = card_type
        self.priority = priority
        self.name = name
        self.rules_text = rules_text
        self.costs = costs if costs else [Cost()]
        self.needs = needs if needs else Icons()
        self.icons = icons if icons else Icons()
        self._markers = 0
        self.costs_paid = []

    @property
    def markers(self):
        return self._markers

    @markers.setter
    def markers(self, value):
        self._markers = value
        if self._markers < 0:
            self._markers = 0

    def when_played(self, game, tableau):
        pass

    def each_turn(self, game, tableau):
        pass

    def on_discard(self, game, tableau):
        pass

    def end_of_game(self, game, tableau):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return str({
            'card_type': self.card_type,
            'priority': self.priority,
            'name': self.name,
            'rules_text': self.rules_text,
            'costs': self.costs,
            'needs': self.needs,
            'icons': self.icons
        })

class CardType(enum.Enum):
    ACTION = 1
    THUG = 2
    HOLDING = 3

class Cost:
    # TODO: Namedtuple?
    def __init__(self, cash=0, thugs=0, holdings=0, cards=0):
        self.cash = cash
        self.thugs = thugs
        self.holdings = holdings
        self.cards = cards

    def __repr__(self):
        return str({
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings,
            'cards': self.cards
        })

class Icons:
    def __init__(self, guns=0, cars=0, keys=0, alcohol=0, hearts=0, wrenches=0, cash=0, thugs=0, holdings=0):
        self.guns = guns
        self.cars = cars
        self.keys = keys
        self.alcohol = alcohol
        self.hearts = hearts
        self.wrenches = wrenches
        self.cash = cash
        self.thugs = thugs
        self.holdings = holdings

    def __eq__(self, other):
        return (True if self.guns == other.guns and
                self.cars == other.cars and
                self.keys == other.keys and
                self.alcohol == other.alcohol and
                self.hearts == other.hearts and
                self.wrenches == other.wrenches and
                self.cash == other.cash and
                self.thugs == other.thugs and
                self.holdings == other.holdings else False)

    def __lt__(self, other):
        return (True if self.guns < other.guns and
                self.cars < other.cars and
                self.keys < other.keys and
                self.alcohol < other.alcohol and
                self.hearts < other.hearts and
                self.wrenches < other.wrenches and
                self.cash < other.cash and
                self.thugs < other.thugs and
                self.holdings < other.holdings else False)

    def __le__(self, other):
        return (True if self.guns <= other.guns and
                self.cars <= other.cars and
                self.keys <= other.keys and
                self.alcohol <= other.alcohol and
                self.hearts <= other.hearts and
                self.wrenches <= other.wrenches and
                self.cash <= other.cash and
                self.thugs <= other.thugs and
                self.holdings <= other.holdings else False)

    def __add__(self, other):
        return Icons(
            self.guns + other.guns,
            self.cars + other.cars,
            self.keys + other.keys,
            self.alcohol + other.alcohol,
            self.hearts + other.hearts,
            self.wrenches + other.wrenches,
            self.cash + other.cash,
            self.thugs + other.thugs,
            self.holdings + other.holdings
        )

    def __repr__(self):
        return str({
            'guns': self.guns,
            'cars': self.cars,
            'keys': self.keys,
            'alcohol': self.alcohol,
            'hearts': self.hearts,
            'wrenches': self.wrenches,
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings
        })
