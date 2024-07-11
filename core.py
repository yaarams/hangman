from dataclasses import dataclass, field
from typing import Set

@dataclass
class Player:
    """Class for keeping track of player score."""
    name: str
    score: int = 0

    def updateScore(self, count: int = 1):
        self.score = self.score + count

@dataclass
class GameState:
    """Class for keeping track of game state."""
    word: str
    guessed_letters: Set[chr] = field(default_factory=set)

    def printCurrentState(self):
        display = ''.join([letter if letter in self.guessed_letters else '_' for letter in self.word])
        print(display)
        print(f"Guessed Letters: {list(self.guessed_letters)}")
