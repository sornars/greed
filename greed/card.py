class Card:
    def __init__(self, name, priority, cost=None, needs=None, rules=None,
                 icons=None, when_played=None, next_turn=None, each_turn=None,
                 end_of_game=None):
        self.name = name
        self.priority = priority
        self.cost = cost
        self.needs = Icons() if needs is None else needs
        self.rules = rules
        self.icons = Icons() if icons is None else icons
        self.when_played = when_played
        self.next_turn = next_turn
        self.each_turn = each_turn
        self.end_of_game = end_of_game


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

    def __repr__(self):
        return str(
            {
                'guns': self.guns,
                'cars': self.cars,
                'keys': self.keys,
                'alcohol': self.alcohol,
                'hearts': self.hearts,
                'wrenches': self.wrenches
            }
            )


class ThugIcons(Icons):
    def __init__(self, guns=0, cars=0, keys=0):
        super().__init__(guns=guns, cars=cars, keys=keys)


class HoldingIcons(Icons):
    def __init__(self, alcohol=0, hearts=0, wrenches=0):
        super().__init__(alcohol=alcohol, hearts=hearts, wrenches=wrenches)
