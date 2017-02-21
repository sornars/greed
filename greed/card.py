import enum

class Card:
    def __init__(self, card_type, name, priority, rules='', costs=None, needs=None,
                 icons=None, when_played=None, passive=None, each_turn=None, end_of_game=None):
        if card_type not in CardType:
            raise ValueError('Invalid card_type')
        self.card_type = card_type
        self.name = name
        self.priority = priority
        self.rules = rules
        self.costs = [Cost()] if costs is None else costs
        self.needs = Icons() if needs is None else needs
        self.icons = Icons() if icons is None else icons
        self.when_played = (lambda x: None) if when_played is None else when_played
        self.passive = (lambda x: None) if passive is None else passive
        self.each_turn = (lambda x: None) if each_turn is None else each_turn
        self.end_of_game = (lambda x: None) if end_of_game is None else end_of_game
        self.markers = 0

    def __repr__(self):
        return self.name

class CardType(enum.Enum):
    ACTION = 1
    THUG = 2
    HOLDING = 3

class Cost:
    # TODO: Namedtuple?
    def __init__(self, cash=0, thugs=0, holdings=0):
        self.cash = cash
        self.thugs = thugs
        self.holdings = holdings

    def __repr__(self):
        return str({
            'cash': self.cash,
            'thugs': self.thugs,
            'holdings': self.holdings
        })


class Icons:
    def __init__(self, guns=0, cars=0, keys=0, alcohol=0, hearts=0, wrenches=0):
        self.guns = guns
        self.cars = cars
        self.keys = keys
        self.alcohol = alcohol
        self.hearts = hearts
        self.wrenches = wrenches

    def __le__(self, other):
        return (True if self.guns <= other.guns and
                self.cars <= other.cars and
                self.keys <= other.keys and
                self.alcohol <= other.alcohol and
                self.hearts <= other.hearts and
                self.wrenches <= other.wrenches else False)

    def __add__(self, other):
        return Icons(
            self.guns + other.guns,
            self.cars + other.cars,
            self.keys + other.keys,
            self.alcohol + other.alcohol,
            self.hearts + other.hearts,
            self.wrenches + other.wrenches
            )

    def __repr__(self):
        return str({
            'guns': self.guns,
            'cars': self.cars,
            'keys': self.keys,
            'alcohol': self.alcohol,
            'hearts': self.hearts,
            'wrenches': self.wrenches
        })


