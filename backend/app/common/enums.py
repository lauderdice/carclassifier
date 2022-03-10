import enum

class Environment(enum.Enum):
    Development = "development"
    Production = "production"
    Beta = "beta"
    Local = "local"

class ClassificationPosition(enum.Enum):
    FirstPosition = 0
    SecondPosition = 1
    ThirdPosition = 2