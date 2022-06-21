"""Models teams of participants"""

from enum import Enum, unique
import random
import string
from model.pymongo_model import SimpleModel

from user import User
from app import mongo, config

@unique
class TeamLevel(Enum):
    """Enumerates the "weight classes" that a team can participate in"""

    JUNIOR_VARSITY = 1
    VARSITY = 2
    PSYCHO_KILLER = 3   # Qu'est-ce que c'est, better run run run run...

@unique
class TeamStatus(Enum):
    """Handles states of approval, participation, disqualification, & elimination"""

    UNAPPROVED = 0
    DISQUALIFIED = 1
    ELIMINATED = 2
    PARTICIPATING = 3


class Team(SimpleModel):
    """Models a team"""

    collection = mongo.db.teams

    @classmethod
    def genSecret() -> str:  # Should be crypto-safe; see https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits/23728630#23728630
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(config.TEAM_SECRET_LENGTH))

    def __init__(self, name: str, weightClass: TeamLevel, members: list = [],
                    score: int = 0, strikes: int = 0, status: TeamStatus = TeamStatus.UNAPPROVED,
                    secret: str = genSecret()):
        self.name = name
        self.weightClass = weightClass
        self.members = members
        self.status = status
        self._strikes = strikes
        self._score = score
    
    def add_member(self, member: User):
        if not member in self.members:
            self.members += [member]
    
    def drop_member(self, member: User) -> bool:
        if not member in self.members:
            return False
        self.members.remove(member)
        return True
    
    @property
    def score(self):
        return self._score
    
    @property
    def strikes(self):
        return self._strikes