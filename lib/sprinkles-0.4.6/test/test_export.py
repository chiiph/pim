import sprinkles

class TestSprinkle(sprinkles.Sprinkle):
    party = "fun"

class SecondTestSprinkle(sprinkles.Sprinkle):
    party = "time"

class HiddenTestSprinkle(sprinkles.Sprinkle):
    party = "food"

_export = [TestSprinkle, SecondTestSprinkle]
