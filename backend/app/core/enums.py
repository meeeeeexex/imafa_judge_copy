import enum


class Role(str, enum.Enum):
    DON = "DON"
    SHERIFF = "SHERIFF"
    MAFIA = "MAFIA"
    CIVILIAN = "CIVILIAN"


class Team(str, enum.Enum):
    RED = "RED"
    BLACK = "BLACK"


RED_ROLES = {Role.SHERIFF, Role.CIVILIAN}
BLACK_ROLES = {Role.DON, Role.MAFIA}
