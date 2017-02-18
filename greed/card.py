class Card:
    def __init__(self, name, priority, cost=None, needs=None, rules=None, icons=None):
        self.name = name
        self.priority = priority
        self.cost = cost
        self.needs = needs
        self.rules = rules
        self.icons = icons


class Action(Card):
    def __init__(self, name, priority, cost, needs, rules):
        super().__init__(name, priority, cost, needs, rules, Icons())


class Rule:
    def __init__(self, text):
        self.text = text


class Icons:
    def __init__(self, guns=0, cars=0, keys=0, alcohol=0, hearts=0, wrenches=0):
        self.guns = guns
        self.cars = cars
        self.keys = keys
        self.alcohol = alcohol
        self.hearts = hearts
        self.wrenches = wrenches

    def __lt__(self, other):
        return (True if self.guns < other.guns or
                self.cars < other.cars or
                self.keys < other.keys or
                self.alcohol < other.alcohol or
                self.hearts < other.hearts or
                self.wrenches < other.wrenches else False)


class ThugIcons(Icons):
    def __init__(self, guns=0, cars=0, keys=0):
        super().__init__(guns=guns, cars=cars, keys=keys)


class HoldingIcons(Icons):
    def __init__(self, alcohol=0, hearts=0, wrenches=0):
        super().__init__(alcohol=alcohol, hearts=hearts, wrenches=wrenches)
